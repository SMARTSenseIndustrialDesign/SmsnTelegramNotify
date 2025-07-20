import logging
import queue
import requests
import threading
import time
from datetime import datetime
from io import BytesIO
import toml
from pathlib import Path

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

class TelegramNotify:

    def __init__(self, token=None, chat_id=None, config_path=None):
        self.START_TIME = None
        self.TG_TIME_INTERVAL = 1  # Default 1 second
        self.thread_local = threading.local()
        self._queue = queue.Queue(maxsize=100)
        self._worker = threading.Thread(target=self._process_queue, daemon=True)
        self._worker.start()

        # โหลด config path ถ้ายังไม่ได้กำหนด
        if config_path is None:
            config_path = self.get_default_config_path()

        # 🔥 Load config ถ้าไม่มี token หรือ chat_id
        if not token or not chat_id:
            cfg = self.load_toml_config(config_path)['telegram_notify']
            self.TG_TOKEN = token if token else cfg['token']
            self.CHAT_ID = chat_id if chat_id else cfg['chat_id']
            self.TG_TIME_INTERVAL = cfg.get('notify_interval_sec', 1)
        else:
            self.TG_TOKEN = token
            self.CHAT_ID = chat_id

    def get_default_config_path(self):
        """Return the default configuration file path."""
        root_project = Path(__file__).resolve().parent.parent
        return root_project / "config.toml"

    def load_toml_config(self, path_file):
        with open(path_file, 'r', encoding="utf-8") as f:
            cfg = toml.load(f)
        return cfg

    def _get_session(self):
        """Return a thread-local requests session."""
        if not hasattr(self.thread_local, "session"):
            self.thread_local.session = requests.Session()
        return self.thread_local.session

    def tg_send_text(self, msg):
        url = f"https://api.telegram.org/bot{self.TG_TOKEN}/sendMessage"
        data = {'chat_id': self.CHAT_ID, 'text': msg}
        session = self._get_session()
        session.post(url, data=data)

    def tg_send_image_bytes(self, msg, image_bytes):
        url = f"https://api.telegram.org/bot{self.TG_TOKEN}/sendPhoto"
        try:
            img = {'photo': image_bytes}
            data = {'chat_id': self.CHAT_ID, 'caption': msg}
            session = self._get_session()
            session.post(url, files=img, data=data)
        except Exception as e:
            logging.exception("Failed to send image bytes: %s", e)

    def tg_send_file(self, msg, path_file):
        try:
            with open(path_file, 'rb') as myfile:
                url = f"https://api.telegram.org/bot{self.TG_TOKEN}/sendDocument"
                files = {'document': myfile}
                data = {'chat_id': self.CHAT_ID, 'caption': msg}
                session = self._get_session()
                session.post(url, files=files, data=data)
        except Exception as e:
            logging.exception("Failed to send file: %s", e)

    def tg_send_video(self, msg, path_file):
        try:
            with open(path_file, 'rb') as myfile:
                url = f"https://api.telegram.org/bot{self.TG_TOKEN}/sendVideo"
                files = {'video': myfile}
                data = {'chat_id': self.CHAT_ID, 'caption': msg}
                session = self._get_session()
                session.post(url, files=files, data=data)
        except Exception as e:
            logging.exception("Failed to send video: %s", e)

    def tg_send_frame_image(self, msg, frame):
        if not HAS_CV2:
            raise ImportError("cv2 not installed. Cannot send frame as image.")

        try:
            ret, img_buf_arr = cv2.imencode(".jpg", frame)
            if ret:
                img = {'photo': img_buf_arr.tobytes()}
                data = {'chat_id': self.CHAT_ID, 'caption': msg}
                session = self._get_session()
                session.post(f"https://api.telegram.org/bot{self.TG_TOKEN}/sendPhoto", files=img, data=data)
        except Exception as e:
            logging.exception("Failed to send frame image: %s", e)

    def tg_frame_send_file(self, msg, frame):
        if not HAS_CV2:
            raise ImportError("cv2 not installed. Cannot send frame as file.")

        try:
            ret, buffer = cv2.imencode(".jpg", frame)
            if ret:
                img_io = BytesIO(buffer)
                img_io.seek(0)
                url = f"https://api.telegram.org/bot{self.TG_TOKEN}/sendDocument"
                files = {'document': ('frame.jpg', img_io, 'image/jpeg')}
                data = {'chat_id': self.CHAT_ID, 'caption': msg}
                session = self._get_session()
                session.post(url, files=files, data=data)
        except Exception as e:
            logging.exception("Failed to send frame file: %s", e)

    # --- start_send ---  
    def start_send_text(self, msg, time_interval_sec=None):
        self._start_send(self.tg_send_text, msg, time_interval_sec=time_interval_sec)

    def start_send_image_bytes(self, msg, image_bytes, time_interval_sec=None):
        self._start_send(self.tg_send_image_bytes, msg, image_bytes, time_interval_sec=time_interval_sec)


    def start_send_file(self, msg, path_file, time_interval_sec=None):
        self._start_send(self.tg_send_file, msg, path_file, time_interval_sec)

    def start_send_video(self, msg, path_file, time_interval_sec=None):
        self._start_send(self.tg_send_video, msg, path_file, time_interval_sec)

    def start_send_frame_image(self, msg, frame, time_interval_sec=None):
        if not HAS_CV2:
            raise ImportError("cv2 not installed. Cannot start send frame as image.")
        self._start_send(self.tg_send_frame_image, msg, frame, time_interval_sec)

    def start_frame_send_file(self, msg, frame, time_interval_sec=None):
        if not HAS_CV2:
            raise ImportError("cv2 not installed. Cannot start send frame as file.")
        self._start_send(self.tg_frame_send_file, msg, frame, time_interval_sec)


    def _start_send(self, func, *args, time_interval_sec=None):
        interval = time_interval_sec if time_interval_sec is not None else self.TG_TIME_INTERVAL
        if self._queue.full():
            logging.warning("Message queue is full, waiting for available slot")
        self._queue.put((func, args, interval))

    def _process_queue(self):
        while True:
            func, args, interval = self._queue.get()
            now = datetime.now()
            if self.START_TIME is None:
                self.START_TIME = now
            else:
                diff = (now - self.START_TIME).total_seconds()
                if diff < interval:
                    time.sleep(interval - diff)
            try:
                func(*args)
            except Exception as e:
                logging.exception("Failed to process queued message: %s", e)
            self.START_TIME = datetime.now()
            self._queue.task_done()
