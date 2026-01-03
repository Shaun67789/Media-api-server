import os, subprocess, uuid

DOWNLOAD_DIR = "downloads"
MAX_SIZE = 400 * 1024 * 1024

def download_media(url, media_type):
    uid = str(uuid.uuid4())
    out = f"{DOWNLOAD_DIR}/{uid}.%(ext)s"

    base_cmd = [
        "yt-dlp",
        "--config-location", "yt.conf",
        "--user-agent", "Mozilla/5.0",
        "-o", out
    ]

    if media_type == "mp3":
        base_cmd += ["-x", "--audio-format", "mp3"]
    else:
        base_cmd += ["-f", "bv*+ba/best"]

    base_cmd.append(url)

    process = subprocess.run(base_cmd, capture_output=True, text=True)

    if process.returncode != 0:
        raise Exception(process.stderr)

    files = os.listdir(DOWNLOAD_DIR)
    latest = max([os.path.join(DOWNLOAD_DIR, f) for f in files], key=os.path.getctime)

    if os.path.getsize(latest) > MAX_SIZE:
        os.remove(latest)
        raise Exception("File exceeds 400MB limit")

    return latest
