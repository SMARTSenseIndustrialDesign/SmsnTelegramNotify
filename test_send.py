from telegram_notify import TelegramNotify

if __name__ == "__main__":
    
    tele_noti = TelegramNotify(config_path="config.toml")
    
    msg = "Hello, World"
    
    tele_noti.start_send_text(msg,)

