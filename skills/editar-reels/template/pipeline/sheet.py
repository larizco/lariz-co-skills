"""Prancha de revisão: frames de um vídeo em mosaico, para conferir com a ferramenta Read.

Uso: python sheet.py <video.mp4> <saida.png> --times 0 1.9 7.3 ... [--cols 6] [--width 216]
"""
import argparse
from pathlib import Path

from common import ffmpeg


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("video", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--times", type=float, nargs="+", required=True)
    ap.add_argument("--cols", type=int, default=6)
    ap.add_argument("--width", type=int, default=216)
    ap.add_argument("--fps", type=float, default=30)
    args = ap.parse_args()

    frames = "+".join(f"eq(n\\,{round(t * args.fps)})" for t in args.times)
    rows = -(-len(args.times) // args.cols)
    ffmpeg("-i", str(args.video), "-vf", f"select='{frames}',scale={args.width}:-1,tile={args.cols}x{rows}",
           "-frames:v", "1", "-update", "1", str(args.out))
    print(args.out)


if __name__ == "__main__":
    main()
