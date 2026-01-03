import os, time, shutil

DOWNLOAD_DIR = "downloads"
MAX_AGE = 20 * 60

def cleanup_loop():
    while True:
        now = time.time()
        for f in os.listdir(DOWNLOAD_DIR):
            path = os.path.join(DOWNLOAD_DIR, f)
            if os.path.isfile(path) and now - os.path.getmtime(path) > MAX_AGE:
                os.remove(path)
        time.sleep(300)
