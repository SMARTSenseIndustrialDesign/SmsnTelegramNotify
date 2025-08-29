from smsn_telegram_notify import TelegramNotify
import time

if __name__ == "__main__":
    
    tele_noti = TelegramNotify(config_path="config.toml")
    
    msg = "Hello, World"
    
    tele_noti.start_send_text(msg,)

    # ❗️รอให้ข้อความถูกส่งก่อนโปรแกรมจบ
    time.sleep(2)

