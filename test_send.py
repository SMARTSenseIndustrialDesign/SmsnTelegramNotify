from TelegramNotify import TelegramNotify
import os

if __name__ == "__main__":
    
    tele_noti = TelegramNotify()
    
    msg = "Hello, World"
    
    tele_noti.start_telegram_notify(msg)

