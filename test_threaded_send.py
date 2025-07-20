import threading
import time
from smsn_telegram.TelegramNotify import TelegramNotify

class MockTelegramNotify(TelegramNotify):
    def tg_send_text(self, msg):
        print(f"{threading.current_thread().name} send at {time.time():.2f}: {msg}")

if __name__ == "__main__":
    tele_noti = MockTelegramNotify(token="dummy", chat_id="dummy")
    tele_noti.TG_TIME_INTERVAL = 0.5

    def worker():
        for _ in range(3):
            tele_noti.start_send_text("Hello", time_interval_sec=0.5)
            time.sleep(0.1)

    threads = [threading.Thread(target=worker, name=f"worker-{i}") for i in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
