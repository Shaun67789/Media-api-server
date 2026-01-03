from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import asyncio
from utils import download_with_ytdlp, download_instagram_post, clear_downloads, DOWNLOAD_DIR
import os

app = FastAPI(title="All Platforms Media Downloader API")

# Start cleanup task
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(clear_downloads())

@app.get("/{platform}")
async def download_media(platform: str, url: str, type: str = "mp4"):
    try:
        platform = platform.lower()

        # Instagram-specific handler
        if platform in ["instagram", "reels", "stories"]:
            info = download_instagram_post(url, type)
        # yt-dlp universal handler for all other platforms
        elif platform in ["youtube", "tiktok", "facebook", "twitter", "shorts", "pinterest"]:
            info = download_with_ytdlp(url, type)
        else:
            # fallback: yt-dlp supports most platforms
            info = download_with_ytdlp(url, type)

        return JSONResponse({
            "status": "success",
            "platform": platform,
            "title": info["title"],
            "channel": info["channel"],
            "duration": info["duration"],
            "size_mb": info["size_mb"],
            "download_url": f"/download/{os.path.basename(info['file_path'])}"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def get_file(filename: str):
    path = os.path.join(DOWNLOAD_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, filename=filename)
