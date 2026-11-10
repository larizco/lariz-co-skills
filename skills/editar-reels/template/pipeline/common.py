import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VIDEOS_DIR = ROOT / "remotion" / "public" / "videos"

_WINGET_FFMPEG = Path(os.environ.get("LOCALAPPDATA", "")) / (
    "Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-9.0.2-full_build/bin"
)


def ffmpeg_bin_dir() -> Path:
    found = shutil.which("ffmpeg")
    if found:
        return Path(found).parent
    if (_WINGET_FFMPEG / "ffmpeg.exe").exists():
        return _WINGET_FFMPEG
    raise SystemExit("ffmpeg não encontrado: instale (winget install Gyan.FFmpeg) ou coloque no PATH")


def ensure_ffmpeg_on_path() -> None:
    bin_dir = str(ffmpeg_bin_dir())
    if bin_dir not in os.environ["PATH"]:
        os.environ["PATH"] = bin_dir + os.pathsep + os.environ["PATH"]


def ffmpeg(*args: str) -> None:
    ensure_ffmpeg_on_path()
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def ffprobe_duration(path: Path) -> float:
    ensure_ffmpeg_on_path()
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(out.stdout.strip())


def replace_with_retry(src: Path, dst: Path, attempts: int = 20) -> None:
    # antivírus/indexador do Windows segura arquivos recém-escritos por alguns segundos
    import time
    for i in range(attempts):
        try:
            src.replace(dst)
            return
        except PermissionError:
            if i == attempts - 1:
                raise
            time.sleep(1.5)
