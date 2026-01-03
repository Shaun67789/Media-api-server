import os, time, threading

DOWNLOAD_DIR = "downloads"
MAX_AGE = 20 * 60  # 20 minutes

def _cleanup_loop():
    while True:
        now = time.time()
        for f in os.listdir(DOWNLOAD_DIR):
            path = os.path.join(DOWNLOAD_DIR, f)
            if os.path.isfile(path) and now - os.path.getmtime(path) > MAX_AGE:
                try:
                    os.remove(path)
                except:
                    pass
        time.sleep(300)

def start_cleaner():
    t = threading.Thread(target=_cleanup_loop, daemon=True)
    t.start()
