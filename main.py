from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from downloader import download_media
from cleanup import start_cleaner
import os

app = FastAPI()

start_cleaner()

@app.get("/{platform}")
async def api_download(platform: str, url: str, type: str = "mp4"):
    try:
        info = download_media(url, type.lower())
        return {
            "status": "success",
            "platform": platform,
            "title": info["title"],
            "channel": info["channel"],
            "duration": info["duration"],
            "size_mb": info["size_mb"],
            "download_url": f"/download/{os.path.basename(info['file'])}"
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/download/{file}")
def get_file(file: str):
    path = f"downloads/{file}"
    if not os.path.exists(path):
        raise HTTPException(404, "File not found")
    return FileResponse(path, filename=file)
