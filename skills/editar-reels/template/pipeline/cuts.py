"""Detecta os cortes (jump cuts) do vídeo pela diferença entre frames consecutivos.

Uso: python cuts.py <video> [--thr 6]
Imprime uma linha por corte (s) e no fim a lista pronta para `rebuild_audio.py --cuts`.
Sequências de picos seguidos (ela se mexendo muito / câmera mexendo) viram um único "cluster" marcado com '?':
nesses, confira a fronteira do resync.json mais próxima e use ela.
"""
import argparse
import subprocess

import numpy as np

from common import ensure_ffmpeg_on_path

W, H = 96, 54

ap = argparse.ArgumentParser()
ap.add_argument("video")
ap.add_argument("--thr", type=float, default=6.0, help="múltiplos da mediana da diferença entre frames")
ap.add_argument("--resync", default=None, help="resync.json: fronteiras de áudio sem corte visual perto ganham o maior pico de imagem próximo")
a = ap.parse_args()
ensure_ffmpeg_on_path()
num, den = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate",
                           "-of", "csv=p=0", a.video], capture_output=True, text=True, check=True).stdout.strip().split("/")
FPS = float(num) / float(den or 1)  # o CapCut pode exportar 30, 29.97 ou 60
p = subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-vf", f"scale={W}:{H},format=gray", "-f", "rawvideo", "-"],
                   capture_output=True, check=True)
fr = np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W).astype(np.float32)
d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))
spikes = [(i + 1) / FPS for i in np.where(d > max(a.thr * np.median(d), 4.0))[0]]
clusters: list[list[float]] = []
for s in spikes:
    if clusters and s - clusters[-1][-1] <= 0.5:
        clusters[-1].append(s)
    else:
        clusters.append([s])
extra = []
if a.resync:
    import json
    segs = json.load(open(a.resync, encoding="utf-8"))["segments"]
    for b in [g["start"] for g in segs[1:]]:
        if not any(abs(c[0] - b) < 1.2 for c in clusters):
            lo, hi = int((b - 1.2) * FPS), int((b + 1.2) * FPS)
            k = lo + int(np.argmax(d[lo:hi]))
            extra.append((k + 1) / FPS)
for e in extra:
    clusters.append([e])
clusters.sort()
cuts = []
for c in clusters:
    flag = "  ?  (cluster %.2f–%.2f: movimento ou corte? confira)" % (c[0], c[-1]) if len(c) > 2 else ""
    if c[0] in extra:
        flag = "  +  (achado pela fronteira do resync.json, pico menor)"
    print(f"{c[0]:.3f}{flag}")
    cuts.append(c[0])
print("\n--cuts " + " ".join(f"{c:.3f}" for c in cuts))
