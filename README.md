# telegram_notify


Config parameters in the repository root

```
[telegram_notify]
    token = "YOUR_TOKEN_HERE"
    chat_id = "YOUR_CHAT_ID"  # Replace with your actual group chat ID
    notify_interval_sec = 60
```

```
from smsn_telegram.TelegramNotify import TelegramNotify
object = TelegramNotify()
```

Or define parameters in code

```
from smsn_telegram.TelegramNotify import TelegramNotify
object = TelegramNotify('YOUR_TOKEN','YOUR_CHAT_ID',True,10)
```

For no interval time

```
define in code:
    object = TelegramNotify('YOUR_TOKEN','YOUR_CHAT_ID',is_interval=False)
```


<hr>
Start notify

```
object.start_send_text('hello')
object.start_send_image('test',cv2.imread('test.jpg') or frame)
object.start_send_file('test', 'test.jpg')
object.start_send_video('test', 'test.mp4')
```
