import os
from yt_dlp import YoutubeDL

DOWNLOAD_DIR = "downloads"
MAX_SIZE_MB = 400

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def safe_filename(name):
    return "".join(c if c.isalnum() or c in "._- " else "_" for c in name)

def file_ok(path):
    return os.path.exists(path) and os.path.getsize(path) <= MAX_SIZE_MB * 1024 * 1024

def download_media(url, media_type):
    ydl_opts = {
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "merge_output_format": "mp4",
        "cookiefile": "cookies.txt"
    }

    if media_type == "mp3":
        ydl_opts["format"] = "bestaudio/best"
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    else:
        ydl_opts["format"] = "bestvideo+bestaudio/best"

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file = ydl.prepare_filename(info)

    if media_type == "mp3":
        file = os.path.splitext(file)[0] + ".mp3"

    file = f"{DOWNLOAD_DIR}/{safe_filename(os.path.basename(file))}"

    if not file_ok(file):
        if os.path.exists(file): os.remove(file)
        raise Exception("File exceeds 400MB limit")

    return {
        "title": info.get("title"),
        "channel": info.get("uploader") or info.get("creator"),
        "duration": info.get("duration"),
        "file": file,
        "size_mb": round(os.path.getsize(file) / (1024 * 1024), 2)
    }
