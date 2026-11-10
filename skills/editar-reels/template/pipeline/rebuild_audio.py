"""Remonta o audio.wav corte a corte (substitui a montagem do resync.py, que acumulava atraso).

1. Cortes do vídeo detectados pela imagem (jump cuts) -> cada "clip" tem UM offset na gravação boa.
2. Offset de partida de cada clip vem do resync.json (pedaço que cobre o meio do clip) e é refinado
   por correlação fina do envelope (±150 ms) só dentro do clip.
3. Cada clip é colocado na POSIÇÃO ABSOLUTA do vídeo (nada de concatenar -> zero deriva).
4. Cauda: no corte, a voz do clip anterior continua até terminar naturalmente (ou até a próxima fala
   começar), com fade — o vídeo corta, o áudio não fica mudo no fim da palavra.
5. Opcional: --replace START:ARQUIVO troca o trecho a partir de START por uma gravação avulsa
   (ex.: "eu espero você lá" regravado), alinhando o início da fala.

Uso: python rebuild_audio.py <slug> --video <cortado.mp4> --raw-audio <gravacao.m4a> --cuts 7.233 21.833 ...
     [--replace 272.367:"frase.m4a"]
"""
import argparse
import json
import tempfile
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf
from scipy import signal

from common import VIDEOS_DIR, ffmpeg

A_SR = 16000
HOP = 40  # 2.5 ms
TAIL_MAX = 0.8
FADE = 0.012


def rms(y: np.ndarray, sr: int, win=0.02) -> np.ndarray:
    n = max(1, int(win * sr))
    return np.sqrt(np.convolve(y.astype(np.float64) ** 2, np.ones(n) / n, mode="same"))


def env(y):
    e = librosa.onset.onset_strength(y=y, sr=A_SR, hop_length=HOP)
    return (e - e.mean()) / (e.std() + 1e-9)


def decode(src: Path, dst: Path, sr=None, mono=False):
    args = ["-i", str(src), "-vn"]
    if mono:
        args += ["-ac", "1"]
    if sr:
        args += ["-ar", str(sr)]
    ffmpeg(*args, str(dst))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--video", required=True, type=Path)
    ap.add_argument("--raw-audio", required=True, type=Path)
    ap.add_argument("--cuts", type=float, nargs="+", required=True)
    ap.add_argument("--replace", default=None)
    a = ap.parse_args()
    out_dir = VIDEOS_DIR / a.slug
    segs = json.loads((out_dir / "resync.json").read_text(encoding="utf-8"))["segments"]

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        decode(a.video, td / "cam16.wav", A_SR, True)
        decode(a.raw_audio, td / "raw16.wav", A_SR, True)
        decode(a.raw_audio, td / "raw.wav")
        cam, _ = librosa.load(td / "cam16.wav", sr=A_SR)
        raw16, _ = librosa.load(td / "raw16.wav", sr=A_SR)
        raw, sr = sf.read(td / "raw.wav", always_2d=True)
        rep = None
        if a.replace:
            rs, rf = a.replace.split(":", 1)
            decode(Path(rf), td / "rep.wav", sr)
            rep = (float(rs), sf.read(td / "rep.wav", always_2d=True)[0])

    dur = len(cam) / A_SR
    bounds = [0.0] + sorted(a.cuts) + [dur]
    clips = []
    raw_env = env(raw16)

    def ncc(c_env, off, s):
        i = int(round((s + off) * A_SR / HOP))
        r = raw_env[max(0, i): max(0, i) + len(c_env)]
        if i < 0 or len(r) < len(c_env):
            return -1.0
        return float(np.corrcoef(c_env, r)[0, 1])

    for s, e in zip(bounds, bounds[1:]):
        reliable = [g for g in segs if g["source"] == "raw_mic"]
        # pedaço do resync que mais se sobrepõe ao clip
        best = max(reliable, key=lambda g: min(e, g["end"]) - max(s, g["start"]))
        off = best["offset"]
        # confere contra uma busca na gravação inteira (clip curto ou sem casamento confiável herdava o offset do vizinho)
        c_env = env(cam[int(s * A_SR):int(e * A_SR)])
        # candidatos: offset do resync, offsets de todos os pedaços confiáveis (continuação de uma fala vizinha
        # é o caso mais comum) e os 5 maiores picos da busca global; vence a maior similaridade real (NCC),
        # não o maior pico bruto (que já casou uma tosse no lugar da fala)
        corr_g = signal.correlate(raw_env, c_env, mode="valid", method="fft")
        peaks = []
        for k in np.argsort(corr_g)[::-1]:
            o = k * HOP / A_SR - s
            if all(abs(o - x) > 1.0 for x in peaks):
                peaks.append(o)
            if len(peaks) == 5:
                break
        cands = [off] + [g["offset"] for g in reliable] + peaks
        scores = [(ncc(c_env, o, s), o) for o in cands]
        n_coarse = scores[0][0]
        n_global, best_off = max(scores)
        if n_global > n_coarse + 0.03:
            off = best_off
        # refino fino dentro do clip
        cs, ce = int(s * A_SR), int(e * A_SR)
        ce_env = env(cam[cs:ce])
        lo = int((s + off - 0.15) * A_SR)
        hi = int((e + off + 0.15) * A_SR)
        re_env = env(raw16[max(0, lo):hi])
        corr = signal.correlate(re_env, ce_env, mode="valid", method="fft")
        k = int(np.argmax(corr))
        refined = (max(0, lo) / A_SR + k * HOP / A_SR) - s
        if abs(refined - off) > 0.16:
            refined = off
        clips.append({"start": s, "end": e, "offset": refined, "coarse": off, "match": round(max(n_coarse, n_global), 2)})

    # ── refino da posição de cada corte pelo áudio: o corte "visual" pode estar errado (picos fracos deduzidos
    # do resync caíram até 0,7 s fora). Procura, em ±0,8 s, o instante em que a fala da câmera deixa de bater
    # com a tentativa A e passa a bater com a tentativa B. Clips vizinhos com o mesmo offset são fundidos.
    def lev100(y, sr_):
        n = int(sr_ / 100)
        return np.sqrt(np.convolve(y.astype(np.float64) ** 2, np.ones(n) / n, mode="same"))[::n]
    cam_l, raw_l = lev100(cam, A_SR), lev100(raw16, A_SR)

    def lncc(t0, t1, off):
        a_ = cam_l[int(t0 * 100):int(t1 * 100)]
        i = int(round((t0 + off) * 100))
        b_ = raw_l[i:i + len(a_)]
        if i < 0 or len(b_) < len(a_) or a_.std() < 1e-6 or b_.std() < 1e-6:
            return 0.0
        return float(np.corrcoef(a_, b_)[0, 1])

    merged = [clips[0]]
    for c in clips[1:]:
        p_ = merged[-1]
        if abs(c["offset"] - p_["offset"]) < 0.08:
            p_["end"] = c["end"]  # mesma tentativa: não há corte de áudio aqui
            continue
        cut0 = c["start"]
        lo_, hi_ = max(p_["start"] + 0.3, cut0 - 0.8), min(c["end"] - 0.3, cut0 + 0.8)
        best_t, best_v = cut0, lncc(cut0 - 0.4, cut0, p_["offset"]) + lncc(cut0, cut0 + 0.4, c["offset"])
        base_v = best_v
        for tt in np.arange(lo_, hi_, 0.01):
            v = lncc(tt - 0.4, tt, p_["offset"]) + lncc(tt, tt + 0.4, c["offset"])
            if v > best_v:
                best_t, best_v = tt, v
        if best_v > base_v + 0.15 and abs(best_t - cut0) > 0.05:
            print(f"corte {cut0:.3f} -> {best_t:.3f} (pelo audio: {base_v:.2f} -> {best_v:.2f})")
            p_["end"] = c["start"] = round(float(best_t), 3)
        merged.append(c)
    clips = merged

    n_out = int(round(dur * sr))
    out = np.zeros((n_out, raw.shape[1]), dtype=np.float64)
    mono = raw.mean(axis=1)
    level = rms(mono, sr)
    thr = np.percentile(level[level > 0], 95) * 0.12

    def place(t0, t1, off, fade_in=FADE, fade_out=FADE):
        i0, i1 = int(round(t0 * sr)), int(round(t1 * sr))
        r0 = int(round((t0 + off) * sr))
        piece = raw[max(0, r0): max(0, r0) + (i1 - i0)].astype(np.float64)
        piece = piece[: max(0, min(len(piece), n_out - i0))]
        if len(piece) == 0:
            return
        g = np.ones(len(piece))
        fi, fo = min(len(g), int(fade_in * sr)), min(len(g), int(fade_out * sr))
        if fi:
            g[:fi] = np.linspace(0, 1, fi)
        if fo:
            g[-fo:] = np.minimum(g[-fo:], np.linspace(1, 0, fo))
        out[i0: i0 + len(piece)] += piece * g[:, None]

    def quiet_from(t, off, limit):
        """primeiro instante >= t em que a gravação (no offset dado) fica em silêncio por 40 ms."""
        i = int((t + off) * sr)
        j = int((limit + off) * sr)
        seg = level[i:j] < thr
        need = int(0.04 * sr)
        run = 0
        for k, q in enumerate(seg):
            run = run + 1 if q else 0
            if run >= need:
                return t + (k - need + 1) / sr
        return limit

    def onset_from(t, off, limit):
        i = int((t + off) * sr)
        j = int((limit + off) * sr)
        idx = np.where(level[i:j] > thr)[0]
        return t + idx[0] / sr if len(idx) else limit

    report = []
    for n, c in enumerate(clips):
        place(c["start"], c["end"], c["offset"])
        tail = 0.0
        if n + 1 < len(clips):
            nxt = clips[n + 1]
            onset_b = onset_from(c["end"], nxt["offset"], c["end"] + TAIL_MAX)
            # a cauda só COMPLETA um som que está terminando. Se logo depois do corte o nível SOBE, é uma sílaba
            # nova começando (ex.: ela começou "po…" e regravou "pode" no clip seguinte) — aí não tem cauda.
            ia = int((c["end"] + c["offset"]) * sr)
            w = int(0.06 * sr)
            before, after = level[max(0, ia - w):ia].mean(), level[ia:ia + w].mean()
            rising = after > before * 1.15 and after > thr
            end_a = quiet_from(c["end"], c["offset"], c["end"] + TAIL_MAX)
            tail_end = min(end_a + 0.05, onset_b - 0.04, c["end"] + 0.35)
            if not rising and tail_end > c["end"] + 0.02:
                place(c["end"] - FADE, tail_end, c["offset"], fade_in=FADE, fade_out=0.05)
                tail = tail_end - c["end"]
        report.append({**{k: round(v, 4) for k, v in c.items()}, "tail": round(tail, 3)})

    if rep is not None:
        t0, y = rep
        i0 = int(t0 * sr)
        out[i0:] *= 0
        lv = rms(y.mean(axis=1), sr)
        on_rep = np.where(lv > np.percentile(lv, 95) * 0.12)[0]
        on_rep = on_rep[0] / sr if len(on_rep) else 0.0
        cam_lv = rms(cam, A_SR)
        seg = cam_lv[int(t0 * A_SR):]
        on_cam = np.where(seg > np.percentile(seg, 95) * 0.15)[0]
        on_cam = on_cam[0] / A_SR if len(on_cam) else 0.0
        start = i0 + int((on_cam - on_rep) * sr)
        if start < i0:  # corta o silêncio inicial da gravação que cairia antes do corte
            y = y[i0 - start:]
            start = i0
        if y.shape[1] != out.shape[1]:
            y = np.repeat(y.mean(axis=1, keepdims=True), out.shape[1], axis=1)
        n = min(len(y), n_out - start)
        g = np.ones(n)
        g[-int(0.06 * sr):] = np.linspace(1, 0, int(0.06 * sr))
        out[start:start + n] += y[:n] * g[:, None]
        report.append({"replace_at": t0, "speech_onset_cam": round(on_cam, 3), "speech_onset_rec": round(on_rep, 3),
                       "rec_len_after_onset": round(len(y) / sr, 3), "room_left": round(dur - t0 - on_cam, 3)})

    peak = np.abs(out).max()
    if peak > 0.99:
        out *= 0.99 / peak
    sf.write(out_dir / "audio.wav", out.astype(np.float32), sr, subtype="PCM_24")
    (out_dir / "rebuild.json").write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    for r_ in report:
        print(r_)


if __name__ == "__main__":
    main()
