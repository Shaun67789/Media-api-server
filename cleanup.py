import os, time, shutil, threading

DOWNLOAD_DIR = "downloads"

def cleaner():
    while True:
        time.sleep(1200)  # 20 minutes
        for f in os.listdir(DOWNLOAD_DIR):
            path = os.path.join(DOWNLOAD_DIR, f)
            try:
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path)
            except:
                pass

def start_cleaner():
    threading.Thread(target=cleaner, daemon=True).start()
