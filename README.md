# telegram_notify

<h3>setting</h3>
- config in folder utils

```
[telegram_notify]
    token = "7635928850:AAHEK1R9na9MRbw1vJHuXyyHcXmN00Nzx-M"
    chat_id = "-4774966242"  # Replace with your actual group chat ID
    is_interval = true # true is on interval time
    notify_interval_sec = 60
```

- define in code

```
object = TelegramNotify('7568707427:AAE1eFFtPDUsjVwi1X_Q7eYLa--jHQ4hPSY','-4569649679',True,10)
object.start_send_text('hello')
object.start_send_image('test',cv2.imread('test.jpg'))
object.start_send_file('test', 'test.jpg')
object.start_send_video('test', 'test.mp4')
```
