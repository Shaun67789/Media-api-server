from fastapi import FastAPI
from downloader import download_media
from cleanup import start_cleaner
import os

app = FastAPI()

os.makedirs("downloads", exist_ok=True)

start_cleaner()

@app.get("/{platform}")
def download(platform: str, url: str, type: str = "mp4"):
    try:
        file_path = download_media(url, type)
        return {
            "platform": platform,
            "status": "success",
            "file": os.path.basename(file_path),
            "size_mb": round(os.path.getsize(file_path) / 1024 / 1024, 2)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
