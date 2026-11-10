"""Modo simples: o vídeo já tem o áudio bom (gravado no próprio celular/câmera ou já trocado no editor).

Copia o vídeo pra pasta do projeto no formato que o Remotion gosta (H.264, fps constante, sem áudio)
e extrai o áudio em WAV. Se a pessoa gravou o áudio num microfone à parte, use resync.py + rebuild_audio.py.

Uso: python prepare.py <slug> --video <video.mp4> [--grade] [--end <segundos>]
  --grade  aplica a mesma correção de cor do resync.py (mostre antes/depois e pergunte antes de usar)
  --end    corta o vídeo nesse segundo (ex.: marca d'água do editor no fim)
Saída em remotion/public/videos/<slug>/: video.mp4 (sem áudio), audio.wav
"""
import argparse
from pathlib import Path

from common import VIDEOS_DIR, ffmpeg, ffprobe_duration, replace_with_retry
from resync import COLOR_GRADE


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--video", required=True, type=Path)
    ap.add_argument("--grade", action="store_true")
    ap.add_argument("--end", type=float)
    ap.add_argument("--fps", type=int, default=30)
    args = ap.parse_args()

    out = VIDEOS_DIR / args.slug
    out.mkdir(parents=True, exist_ok=True)
    cut = ["-t", str(args.end)] if args.end else []
    vf = f"fps={args.fps}" + (f",{COLOR_GRADE}" if args.grade else "")

    ffmpeg("-i", str(args.video), *cut, "-an", "-vf", vf, "-c:v", "libx264", "-preset", "medium",
           "-crf", "16", "-pix_fmt", "yuv420p", str(out / "video.tmp.mp4"))
    replace_with_retry(out / "video.tmp.mp4", out / "video.mp4")
    ffmpeg("-i", str(args.video), *cut, "-vn", "-ac", "2", "-ar", "48000", "-c:a", "pcm_s24le", str(out / "audio.wav"))
    print(f"{out}: video.mp4 {ffprobe_duration(out / 'video.mp4'):.2f}s, audio.wav {ffprobe_duration(out / 'audio.wav'):.2f}s")


if __name__ == "__main__":
    main()
