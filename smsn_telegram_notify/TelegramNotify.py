
import time
import requests
import cv2
from datetime import datetime
import threading
import toml
import os
import logging
from logging.handlers import TimedRotatingFileHandler

class TelegramNotify:

    shared_session = requests.Session()

    def __init__(self, token= None, chat_id= None, is_interval=None, time_interval_sec= None):
        """
        Telegram Notification Class
        """
        cfg_telegram = self.load_toml_config()['telegram_notify']
        self.START_TIME = None
        self.TG_TOKEN = token if token else cfg_telegram['token']
        self.CHAT_ID = chat_id if chat_id else cfg_telegram['chat_id']
        self.IS_INTERVAL = is_interval if is_interval else cfg_telegram['is_interval']
        self.TG_TIME_INTERVAL = time_interval_sec if time_interval_sec else cfg_telegram['notify_interval_sec']
        self.SESSION = TelegramNotify.shared_session
        
        # Logging setup with retention of 7 days
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "telegram_notify.log")
        handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=7, encoding='utf-8')
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger = logging.getLogger()
        logger.setLevel(logging.ERROR)
        logger.addHandler(handler)

    def load_toml_config(self):

        base_dir = os.path.dirname(os.path.abspath(__file__))  # หา path ของ script นี้
        path_file = os.path.join(base_dir, "utils", "config_telegram.toml")
        lock = threading.Lock()
        with lock:
            with open(path_file, 'r') as f:
                cfg = toml.load(f)
        return cfg

    def tg_send_text(self, msg):
        
        url = "https://api.telegram.org/bot" + self.TG_TOKEN +"/sendMessage"
        data = {'chat_id': self.CHAT_ID, 'text': msg}
        session_post = self.SESSION.post(url, data=data)
        if session_post.status_code != 200:
            logging.error(f"Failed to send text: {msg}. Status code: {session_post.status_code}, Response: {session_post.text}")


    def tg_send_image(self, msg, image):
        
        url = "https://api.telegram.org/bot" + self.TG_TOKEN +"/sendPhoto"
        try:
            ret, img_buf_arr = cv2.imencode(".jpg", image)
            if ret:
                image = img_buf_arr.tobytes()
                img = {'photo': image}
                data = {'chat_id': self.CHAT_ID, 'caption': msg}
                session_post = self.SESSION.post(url, files=img, data=data)
                if session_post.status_code != 200:
                    logging.error(f"Failed to send image. Status code: {session_post.status_code}, Response: {session_post.text}")

        except Exception:
            pass

    def tg_send_file(self, msg, path_file):

        url = "https://api.telegram.org/bot" + self.TG_TOKEN +"/sendDocument"
        with open(path_file, 'rb') as myfile:
            file = {'document': myfile}
            data = {'chat_id': self.CHAT_ID, 'caption': msg}
            session_post = self.SESSION.post(url, files=file, data=data)
            if session_post.status_code != 200:
                logging.error(f"Failed to send file {path_file}. Status code: {session_post.status_code}, Response: {session_post.text}")

    def tg_send_video(self, msg, path_file):

        url = "https://api.telegram.org/bot" + self.TG_TOKEN +"/sendVideo"
        with open(path_file, 'rb') as myfile:
            file = {'video': myfile}
            data = {'chat_id': self.CHAT_ID, 'caption': msg}
            session_post = self.SESSION.post(url, files=file, data=data)
            if session_post.status_code != 200:
                logging.error(f"Failed to send video {path_file}. Status code: {session_post.status_code}, Response: {session_post.text}")

    def start_send_text(self, msg):
        
        current_time = datetime.fromtimestamp(time.time())
        if not self.IS_INTERVAL:
            threading.Thread(target= self.tg_send_text, args= (msg,)).start()
            return
        
        if not self.START_TIME or int((current_time - self.START_TIME).total_seconds()) > self.TG_TIME_INTERVAL:
            self.START_TIME = current_time
            threading.Thread(target= self.tg_send_text, args= (msg,)).start()

    def start_send_image(self, msg, image):

        current_time = datetime.fromtimestamp(time.time())

        if not self.IS_INTERVAL:
            threading.Thread(target= self.tg_send_image, args= (msg, image,)).start()
            return
        
        if not self.START_TIME or int((current_time - self.START_TIME).total_seconds()) > self.TG_TIME_INTERVAL:
            self.START_TIME = current_time
            threading.Thread(target= self.tg_send_image, args= (msg, image,)).start()
    

    def start_send_file(self, msg, path_file):

        current_time = datetime.fromtimestamp(time.time())

        if not self.IS_INTERVAL:
            threading.Thread(target= self.tg_send_file, args= (msg, path_file,)).start()
            return
  
        if not self.START_TIME or int((current_time - self.START_TIME).total_seconds()) > self.TG_TIME_INTERVAL:
            self.START_TIME = current_time
            threading.Thread(target= self.tg_send_file, args= (msg, path_file,)).start()

    def start_send_video(self, msg, path_file):
        
        current_time = datetime.fromtimestamp(time.time())

        if not self.IS_INTERVAL:
            threading.Thread(target= self.tg_send_video, args= (msg, path_file,)).start()
            return
  
        if not self.START_TIME or int((current_time - self.START_TIME).total_seconds()) > self.TG_TIME_INTERVAL:
            self.START_TIME = current_time
            threading.Thread(target= self.tg_send_video, args= (msg, path_file,)).start()


    # def start_telegram_notify(self, msg=None, image=None, path_file=None, path_video=None):
    #     """
    #     text: msg
    #     image: msg, image (frame video)
    #     file: msg, path_file
    #     video: msg, path_video
    #     """
    #     current_time = datetime.fromtimestamp(time.time())
    
    #     if not self.START_TIME or int((current_time - self.START_TIME).total_seconds()) > self.TG_TIME_INTERVAL:
    #         self.START_TIME = current_time
    #         if msg:
    #             threading.Thread(target= self.tg_send_text, args= (msg,)).start()
    #         if msg and image:
    #             threading.Thread(target= self.tg_send_image, args= (msg, image,)).start()
    #         if msg and path_file:
    #             threading.Thread(target= self.tg_send_file, args= (msg, path_file,)).start()
    #         if msg and path_video:
    #             threading.Thread(target= self.tg_send_video, args= (msg, path_file,)).start()
        



# x = TelegramNotify('7568707427:AAE1eFFtPDUsjVwi1X_Q7eYLa--jHQ4hPSY','-4569649679',True,10)
# x= TelegramNotify()
# while True:
    # x.start_send_text('hello')
# x.start_send_text('hello')
# x.start_send_image('test',cv2.imread('test.jpg'))
# x.start_send_file('test', 'test.jpg')
# x.start_send_video('test', 'test.mp4')
