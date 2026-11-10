"""Converte o render do Remotion para o padrão do Instagram/YouTube.

O Remotion (frames em JPEG) gera yuvj420p/full range, que pode mostrar preto lavado.
Uso: python finalize.py <render.mp4> <saida.mp4>
"""
import argparse
import json
import subprocess
from pathlib import Path

from common import ensure_ffmpeg_on_path, ffmpeg


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path)
    ap.add_argument("dst", type=Path)
    args = ap.parse_args()

    ffmpeg("-i", str(args.src),
           "-vf", "scale=in_range=full:out_range=tv,format=yuv420p",
           "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high", "-level", "4.2",
           "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
           "-c:a", "copy", "-movflags", "+faststart", str(args.dst))

    ensure_ffmpeg_on_path()
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_name,width,height,r_frame_rate,pix_fmt,color_range,sample_rate",
         "-show_entries", "format=duration,size", "-of", "json", str(args.dst)],
        check=True, capture_output=True, text=True,
    )
    info = json.loads(probe.stdout)
    v = next(s for s in info["streams"] if s.get("width"))
    a = next((s for s in info["streams"] if s.get("sample_rate")), {})
    fmt = info["format"]
    print(f"{args.dst}: {v['width']}x{v['height']} {v['r_frame_rate']} {v['codec_name']} {v['pix_fmt']}/{v.get('color_range')} "
          f"+ {a.get('codec_name')} {a.get('sample_rate')}Hz, {float(fmt['duration']):.1f}s, {int(fmt['size']) / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
