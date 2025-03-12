# telegram_notify

Config parameters in folder utils

```
[telegram_notify]
    token = "7635928850:AAHEK1R9na9MRbw1vJHuXyyHcXmNxxxx"
    chat_id = "-477496xxxx"  # Replace with your actual group chat ID
    is_interval = true # true is on interval time
    notify_interval_sec = 60
```

```
object = TelegramNotify()
```

Or define parameters in code

```
object = TelegramNotify('7568707427:AAE1eFFtPDUsjVwi1X_Q7eYLa--xxxx','-456964xxxx',True,10)
```

For no interval time

```
define in config file:
    is_interval = false 

define in code:
    TelegramNotify('7568707427:AAE1eFFtPDUsjVwi1X_Q7eYLa--xxxx','-456964xxxx',is_interval=False)
```


<hr>
Start notify

```
object.start_send_text('hello')
object.start_send_image('test',cv2.imread('test.jpg') or frame)
object.start_send_file('test', 'test.jpg')
object.start_send_video('test', 'test.mp4')
```
