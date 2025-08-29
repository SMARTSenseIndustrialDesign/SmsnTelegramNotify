# telegram_notify

Library สำหรับส่งข้อความหรือไฟล์ไปยัง Telegram ได้อย่างง่ายดาย

## การติดตั้ง

ติดตั้งจากโค้ดในเครื่อง:

```bash
pip install .
```

## การใช้งาน

```python
from telegram_notify import TelegramNotify

# อ่านค่าจากไฟล์ config.toml
notifier = TelegramNotify(config_path="config.toml")

# หรือกำหนด token และ chat_id โดยตรง
notifier = TelegramNotify(token="YOUR_TOKEN", chat_id="CHAT_ID")

notifier.start_send_text("hello")
```

ไฟล์ `config.toml` ตัวอย่าง:

```toml
[telegram_notify]
  token = "123456:ABCDEFG"
  chat_id = "-100123456"
  notify_interval_sec = 60
```

> ฟังก์ชันส่งรูปภาพและวิดีโอจำเป็นต้องติดตั้ง `opencv-python` เพิ่มเติม

## เริ่มส่งแจ้งเตือน

```python
notifier.start_send_text('hello')
notifier.start_send_image('test', cv2.imread('test.jpg'))
notifier.start_send_file('test', 'test.jpg')
notifier.start_send_video('test', 'test.mp4')
```
