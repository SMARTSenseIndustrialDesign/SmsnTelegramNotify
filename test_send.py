from smsn_telegram.TelegramNotify import TelegramNotify

if __name__ == "__main__":
    
    tele_noti = TelegramNotify()
    
    msg = "Hello, World"
    
    tele_noti.start_send_text(msg)

