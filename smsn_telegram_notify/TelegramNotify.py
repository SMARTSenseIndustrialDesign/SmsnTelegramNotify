
import time
import requests
try:
    import cv2
except ImportError:
    print("cv2 not found, please install opencv-python")
from datetime import datetime
import threading
from io import BytesIO 

class TelegramNotify:

    shared_session = requests.Session()

    def __init__(self, token= None, chat_id= None):
        # cfg_line = AppConfig().load_toml_config()['line_notify']
        self.START_TIME = None
        self.TG_TOKEN = token
        self.CHAT_ID = chat_id
        self.TG_TIME_INTERVAL = 1
        self.session = TelegramNotify.shared_session

    def tg_send_text(self, msg):
        
        url = "https://api.telegram.org/bot" + self.TG_TOKEN +"/sendMessage"
        data = {'chat_id': self.CHAT_ID, 'text': msg}
        session_post = self.session.post(url, data=data)
        # print(session_post.text)

    def tg_send_frame_image(self, msg, frame):
        
        url = "https://api.telegram.org/bot" + self.TG_TOKEN +"/sendPhoto"
        try:
            ret, img_buf_arr = cv2.imencode(".jpg", frame)
            if ret:
                image = img_buf_arr.tobytes()
                img = {'photo': image}
                data = {'chat_id': self.CHAT_ID, 'caption': msg}
                session_post = self.session.post(url, files=img, data=data)
                # print(session_post.text)
        except Exception:
            pass
    
    def tg_send_image_bytes(self, msg, image_bytes):
        
        url = "https://api.telegram.org/bot" + self.TG_TOKEN +"/sendPhoto"
        try:
            img = {'photo': image_bytes}
            data = {'chat_id': self.CHAT_ID, 'caption': msg}
            session_post = self.session.post(url, files=img, data=data)
            # print(session_post.text)
        except Exception:
            pass

    def tg_frame_send_file(self, msg, frame):
        _, buffer = cv2.imencode(".jpg", frame)  # บีบอัดเป็น JPG
        img_io = BytesIO(buffer)  # แปลงเป็น stream
        img_io.seek(0)  # รีเซ็ต pointer

        # ส่งไปยัง Telegram
        url = f"https://api.telegram.org/bot{self.TG_TOKEN}/sendDocument"
        files = {'document': ('frame.jpg', img_io, 'image/jpeg')}
        data = {'chat_id': self.CHAT_ID, 'caption': msg}
        try:
            session_post = self.session.post(url, files=files, data=data)
        except Exception:
            pass
        
    
    def tg_send_file(self, msg, path_file):

        url = "https://api.telegram.org/bot" + self.TG_TOKEN +"/sendDocument"
        with open(path_file, 'rb') as myfile:
            file = {'document': myfile}
            data = {'chat_id': self.CHAT_ID, 'caption': msg}
            session_post = self.session.post(url, files=file, data=data)

    def tg_send_video(self, msg, path_file):

        url = "https://api.telegram.org/bot" + self.TG_TOKEN +"/sendVideo"
        with open(path_file, 'rb') as myfile:
            file = {'video': myfile}
            data = {'chat_id': self.CHAT_ID, 'caption': msg}
            session_post = self.session.post(url, files=file, data=data)


    def start_send_image_bytes(self, msg, image_bytes, time_interval_sec= None):
        if time_interval_sec != None:
            self.LINE_TIME_INTERVAL = time_interval_sec
        current_time = datetime.fromtimestamp(time.time())
  
        if not self.START_TIME or int((current_time - self.START_TIME).total_seconds()) > self.LINE_TIME_INTERVAL:
            self.START_TIME = datetime.fromtimestamp(time.time())
            threading.Thread(target= self.tg_send_image_bytes, args= (msg, image_bytes,)).start()
    
    def start_send_frame_image(self, msg, frame, time_interval_sec= None):
        if time_interval_sec != None:
            self.LINE_TIME_INTERVAL = time_interval_sec
        current_time = datetime.fromtimestamp(time.time())
  
        if not self.START_TIME or int((current_time - self.START_TIME).total_seconds()) > self.LINE_TIME_INTERVAL:
            self.START_TIME = datetime.fromtimestamp(time.time())
            threading.Thread(target= self.tg_send_frame_image, args= (msg, frame,)).start()
    
    def start_send_text(self, msg, time_interval_sec= None):
        if time_interval_sec != None:
            self.LINE_TIME_INTERVAL = time_interval_sec
        current_time = datetime.fromtimestamp(time.time())
    
        if not self.START_TIME or int((current_time - self.START_TIME).total_seconds()) > self.LINE_TIME_INTERVAL:
            self.START_TIME = datetime.fromtimestamp(time.time())
            threading.Thread(target= self.tg_send_text, args= (msg,)).start()

    def start_send_file(self, msg, path_file, time_interval_sec= None):
        if time_interval_sec != None:
            self.LINE_TIME_INTERVAL = time_interval_sec
        current_time = datetime.fromtimestamp(time.time())
  
        if not self.START_TIME or int((current_time - self.START_TIME).total_seconds()) > self.LINE_TIME_INTERVAL:
            self.START_TIME = datetime.fromtimestamp(time.time())
            threading.Thread(target= self.tg_send_file, args= (msg, path_file,)).start()
    
    def start_frame_send_file(self, msg, frame, time_interval_sec= None):
        if time_interval_sec != None:
            self.LINE_TIME_INTERVAL = time_interval_sec
        current_time = datetime.fromtimestamp(time.time())
  
        if not self.START_TIME or int((current_time - self.START_TIME).total_seconds()) > self.LINE_TIME_INTERVAL:
            self.START_TIME = datetime.fromtimestamp(time.time())
            threading.Thread(target= self.tg_frame_send_file, args= (msg, frame,)).start()

    def start_send_video(self, msg, path_file, time_interval_sec= None):
        if time_interval_sec != None:
            self.LINE_TIME_INTERVAL = time_interval_sec
        current_time = datetime.fromtimestamp(time.time())
  
        if not self.START_TIME or int((current_time - self.START_TIME).total_seconds()) > self.LINE_TIME_INTERVAL:
            self.START_TIME = datetime.fromtimestamp(time.time())
            threading.Thread(target= self.tg_send_video, args= (msg, path_file,)).start()



    

# x = TelegramNotify('7568707427:AAE1eFFtPDUsjVwi1X_Q7eYLa--jHQ4hPSY','-4569649679',True,10)
# x= TelegramNotify()
# while True:
    # x.start_send_text('hello')
# x.start_send_text('hello')
# x.start_send_image('test',cv2.imread('test.jpg'))
# x.start_send_file('test', 'test.jpg')
# x.start_send_video('test', 'test.mp4')
