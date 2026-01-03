import os
import shutil
import asyncio
from yt_dlp import YoutubeDL
import instaloader

DOWNLOAD_DIR = "downloads"
MAX_SIZE_MB = 400

# Ensure download folder exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Cleanup task every 20 min
async def clear_downloads():
    while True:
        await asyncio.sleep(20 * 60)
        for file in os.listdir(DOWNLOAD_DIR):
            path = os.path.join(DOWNLOAD_DIR, file)
            try:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
            except Exception as e:
                print(f"Failed to delete {path}: {e}")

# Check file size limit
def file_size_ok(path: str):
    size_mb = os.path.getsize(path) / (1024 * 1024)
    return size_mb <= MAX_SIZE_MB

# Universal downloader using yt-dlp
def download_with_ytdlp(url: str, download_type: str):
    output_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_template,
        'noplaylist': True,
        'quiet': True,
        'merge_output_format': 'mp4',
    }

    if download_type == "mp3":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s')
        })

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)
        if download_type == "mp3":
            file_path = os.path.splitext(file_path)[0] + ".mp3"

        if not file_size_ok(file_path):
            os.remove(file_path)
            raise Exception("File size exceeds 400MB")

        return {
            "title": info.get("title"),
            "channel": info.get("uploader") or info.get("creator"),
            "duration": info.get("duration"),
            "size_mb": round(os.path.getsize(file_path)/(1024*1024),2),
            "file_path": file_path
        }

# Instagram downloader (posts & reels) with mp3 fallback
def download_instagram_post(url: str, download_type: str):
    L = instaloader.Instaloader(dirname_pattern=DOWNLOAD_DIR, download_videos=True,
                                download_video_thumbnails=False, download_geotags=False,
                                download_comments=False, save_metadata=False)
    shortcode = url.strip("/").split("/")[-1]
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    L.download_post(post, target=post.owner_username)
    file_path = os.path.join(DOWNLOAD_DIR, f"{post.owner_username}_{post.shortcode}.mp4")

    if download_type == "mp3":
        # Convert video to mp3 using yt-dlp (re-download audio only)
        return download_with_ytdlp(url, "mp3")

    if not file_size_ok(file_path):
        os.remove(file_path)
        raise Exception("File size exceeds 400MB")

    return {
        "title": post.title or post.shortcode,
        "channel": post.owner_username,
        "duration": None,
        "size_mb": round(os.path.getsize(file_path)/(1024*1024),2),
        "file_path": file_path
    }
