"""Mede o atraso (lag) entre o áudio final (audio.wav) e o áudio da câmera, em janelas deslizantes.
Lag ~0 = sincronizado. Uso: python diag_sync.py <video_com_audio_camera> <audio.wav>"""
import sys, tempfile
from pathlib import Path
import librosa, numpy as np
from scipy import signal
from common import ffmpeg
SR, HOP = 16000, 80
vid, aud = sys.argv[1], sys.argv[2]
with tempfile.TemporaryDirectory() as td:
    c = Path(td) / "c.wav"; a = Path(td) / "a.wav"
    ffmpeg("-i", vid, "-vn", "-ac", "1", "-ar", str(SR), str(c))
    ffmpeg("-i", aud, "-ac", "1", "-ar", str(SR), str(a))
    cam, _ = librosa.load(c, sr=SR); mic, _ = librosa.load(a, sr=SR)
def env(y):
    e = librosa.onset.onset_strength(y=y, sr=SR, hop_length=HOP); return (e - e.mean()) / (e.std() + 1e-9)
ce, me = env(cam), env(mic)
fps = SR / HOP; W = int(2.0 * fps); M = int(0.6 * fps)
t = 0.0
while (t + 2.6) * fps < min(len(ce), len(me)):
    i = int(t * fps)
    w = ce[i:i + W]; seg = me[max(0, i - M): i + W + M]
    if np.std(cam[int(t*SR):int((t+2)*SR)]) < 0.01:
        print(f"{t:7.1f}  (silêncio)"); t += 1; continue
    corr = signal.correlate(seg, w, mode="valid")
    k = int(np.argmax(corr)); lag = (k - (i - max(0, i - M))) / fps
    q = corr[k] / (np.linalg.norm(w) * np.linalg.norm(seg[k:k+W]) + 1e-9)
    print(f"{t:7.1f}  lag={lag*1000:+6.0f}ms  sim={q:.2f}")
    t += 1
