import subprocess
import shlex
from pathlib import Path

from config import DOWNLOAD_DIR

Path(DOWNLOAD_DIR).mkdir(exist_ok=True)

def download_audio(url: str) -> Path:
    """Download audio from YouTube and return Path object."""
    out_template = str(Path(DOWNLOAD_DIR) / "%(title)s.%(ext)s")
    cmd = f'yt-dlp -x --audio-format mp3 -o "{out_template}" {shlex.quote(url)}'
    subprocess.check_call(cmd, shell=True)
    files = list(Path(DOWNLOAD_DIR).glob("*.mp3"))
    return max(files, key=lambda p: p.stat().st_mtime)
