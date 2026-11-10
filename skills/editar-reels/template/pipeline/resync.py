"""Troca o áudio de um vídeo já cortado pelo áudio de um microfone melhor, gravado à parte.

O vídeo já foi editado (erros/respiros removidos), então a gravação externa longa (sem cortes)
não tem um único offset constante em relação ao vídeo: cada pedaço cortado cai num ponto diferente
da gravação. Este script acha, pedaço a pedaço, onde cada trecho do vídeo se encaixa na gravação
externa (por correlação do envelope de onset, robusta a timbre/qualidade diferentes entre os dois
microfones), e monta um áudio final com a duração exata do vídeo, mas com o som do microfone bom.

Uso: python resync.py <slug> --video <cortado.mp4> --raw-audio <gravacao-longa.m4a>
Saída em remotion/public/videos/<slug>/: video.mp4 (cópia, sem áudio), audio.wav, resync.json
"""
import argparse
import json
import tempfile
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf
from scipy import signal

from common import VIDEOS_DIR, ffmpeg, ffprobe_duration, replace_with_retry

SR = 22050          # taxa usada só para a análise/correlação (não para o áudio final)
HOP = 128
WIN = 4.0            # s: janela de sondagem no vídeo cortado
STEP = 1.0           # s: passo entre sondagens
CONF_MIN = 1.15      # pico / 2º pico; abaixo disso a sondagem é descartada (sem fala, ruído, etc.)
OFFSET_TOL = 0.08    # s: offsets mais próximos que isso são "o mesmo pedaço"
FINE_PROBE = 0.25    # s: janela usada para refinar o ponto exato do corte
MIN_PROBES = 2       # pedaços com menos sondagens que isso não têm confirmação suficiente: usa o
                      # áudio original da câmera nesse trecho em vez de arriscar um encaixe errado

# correção de cor OPCIONAL (--grade): tira o amarelado de luz de quarto (paredes/roupas bege deixam a pele
# amarelada), sem upscale por IA — correção clássica de cor + nitidez leve. Mostre antes/depois e pergunte.
COLOR_GRADE = (
    "eq=contrast=1.08:brightness=0.01:saturation=1.08:gamma_r=0.96:gamma_b=1.04,"
    "colorbalance=rs=-0.02:bs=0.05:rm=-0.03:bm=0.05:rh=-0.01:bh=0.02,"
    "unsharp=5:5:0.5:5:5:0.0"
)


def r(x, nd=4):
    return round(float(x), nd)


def onset_env(y: np.ndarray) -> np.ndarray:
    e = librosa.onset.onset_strength(y=y, sr=SR, hop_length=HOP)
    return (e - e.mean()) / (e.std() + 1e-9)


def probe_offset(window_env: np.ndarray, line_env: np.ndarray) -> tuple[float | None, float]:
    """Acha onde `window_env` melhor se encaixa dentro de `line_env`. Retorna (offset_s, confiança)."""
    if len(line_env) < len(window_env):
        return None, 0.0
    corr = signal.correlate(line_env, window_env, mode="valid", method="fft")
    best = int(np.argmax(corr))
    far = np.abs(np.arange(len(corr)) - best) > int(1.0 * SR / HOP)
    second = corr[far].max() if far.any() else 1e-9
    confidence = float(corr[best] / (max(second, 1e-9)))
    return best * HOP / SR, confidence


def sweep(cam_env: np.ndarray, line_env: np.ndarray, cam_dur: float) -> list[dict]:
    probes = []
    t = 0.0
    while t + WIN <= cam_dur:
        a = int(t * SR / HOP)
        b = a + int(WIN * SR / HOP)
        match_time, conf = probe_offset(cam_env[a:b], line_env)
        # probe_offset acha onde a janela cai dentro da gravação externa (tempo absoluto);
        # o offset que nos interessa é o deslocamento constante raw_time - cam_time.
        offset = (match_time - t) if match_time is not None else None
        probes.append({"t": t, "offset": offset, "conf": conf})
        t += STEP
    return probes


def group_segments(probes: list[dict], cam_dur: float) -> list[dict]:
    good = [p for p in probes if p["offset"] is not None and p["conf"] >= CONF_MIN]
    if not good:
        raise SystemExit("não consegui casar nenhum trecho do vídeo com a gravação externa — confira os arquivos")

    runs: list[list[dict]] = [[good[0]]]
    for p in good[1:]:
        if abs(p["offset"] - runs[-1][-1]["offset"]) <= OFFSET_TOL:
            runs[-1].append(p)
        else:
            runs.append([p])

    segs = []
    for run in runs:
        offsets = sorted(x["offset"] for x in run)
        segs.append({
            "offset": offsets[len(offsets) // 2],  # mediana
            "t_first": run[0]["t"],
            "t_last": run[-1]["t"] + WIN,
            "confidence": r(min(x["conf"] for x in run), 2),
            "n_probes": len(run),
        })
    # funde vizinhos cujo offset praticamente não mudou (só perderam confiança no meio)
    merged = [segs[0]]
    for s in segs[1:]:
        if abs(s["offset"] - merged[-1]["offset"]) <= OFFSET_TOL:
            merged[-1]["t_last"] = s["t_last"]
            merged[-1]["confidence"] = min(merged[-1]["confidence"], s["confidence"])
            merged[-1]["n_probes"] += s["n_probes"]
        else:
            merged.append(s)
    merged[0]["t_first"] = 0.0
    merged[-1]["t_last"] = cam_dur
    return merged


def refine_boundary(cam: np.ndarray, line: np.ndarray, lo: float, hi: float, off_a: float, off_b: float) -> float:
    """Varre [lo, hi] (tempo no vídeo) e acha o instante exato em que o trecho deixa de bater com
    `off_a` e passa a bater com `off_b`, comparando a correlação de uma janela curta antes/depois."""
    def score(cam_t0: float, cam_t1: float, line_t0: float) -> float:
        a = cam[int(cam_t0 * SR): int(cam_t1 * SR)]
        b = line[int(line_t0 * SR): int(line_t0 * SR) + len(a)]
        if len(a) == 0 or len(b) < len(a):
            return -1e9
        a = a - a.mean()
        b = b - b.mean()
        na, nb = np.linalg.norm(a), np.linalg.norm(b)
        return float(np.dot(a, b) / (na * nb + 1e-9))

    best_t, best_val = lo, -1e9
    for t in np.arange(lo, hi, 0.02):
        val = (score(max(0, t - FINE_PROBE), t, max(0, t - FINE_PROBE) + off_a)
               + score(t, t + FINE_PROBE, t + off_b))
        if val > best_val:
            best_val, best_t = val, t
    return float(best_t)


def crossfade_append(buf: np.ndarray, piece: np.ndarray, sr: int, fade_s: float = 0.015) -> np.ndarray:
    fade_n = min(int(fade_s * sr), len(buf), len(piece))
    if fade_n <= 0 or len(buf) == 0:
        return np.concatenate([buf, piece])
    ramp = np.linspace(0, 1, fade_n)[:, None] if buf.ndim > 1 else np.linspace(0, 1, fade_n)
    head = buf[:-fade_n]
    mixed = buf[-fade_n:] * (1 - ramp) + piece[:fade_n] * ramp
    return np.concatenate([head, mixed, piece[fade_n:]])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--video", required=True, type=Path)
    ap.add_argument("--raw-audio", required=True, type=Path)
    ap.add_argument("--grade", action="store_true", help="aplica a correção de cor COLOR_GRADE")
    args = ap.parse_args()

    out_dir = VIDEOS_DIR / args.slug
    out_dir.mkdir(parents=True, exist_ok=True)
    video_dur = ffprobe_duration(args.video)

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        cam_wav = tmp / "cam.wav"
        ffmpeg("-i", str(args.video), "-vn", "-ac", "1", "-ar", str(SR), str(cam_wav))
        cam, _ = librosa.load(cam_wav, sr=SR)

        # soundfile/libsndfile não abre .m4a (AAC) direto: decodifica pro WAV primeiro,
        # mantendo a taxa de amostragem nativa pra não perder qualidade no áudio final.
        raw_native_wav = tmp / "raw_native.wav"
        ffmpeg("-i", str(args.raw_audio), str(raw_native_wav))

        raw_wav = tmp / "raw.wav"
        ffmpeg("-i", str(raw_native_wav), "-ac", "1", "-ar", str(SR), str(raw_wav))
        line, _ = librosa.load(raw_wav, sr=SR)

        print(f"vídeo: {video_dur:.1f}s cortado | gravação externa: {len(line) / SR:.1f}s")
        cam_env = onset_env(cam)
        line_env = onset_env(line)

        print("sondando casamento de trechos...")
        probes = sweep(cam_env, line_env, video_dur)
        segments = group_segments(probes, video_dur)
        print(f"{len(segments)} pedaço(s) detectado(s)")

        for s in segments:
            s["reliable"] = s["n_probes"] >= MIN_PROBES

        for i in range(len(segments) - 1):
            a, b = segments[i], segments[i + 1]
            if a["reliable"] and b["reliable"]:
                boundary = refine_boundary(cam, line, a["t_last"] - STEP, b["t_first"] + STEP, a["offset"], b["offset"])
            else:
                # um dos lados não tem offset confiável pra guiar o refino fino por correlação;
                # fecha o limite no meio da zona de incerteza pra não sobrepor nem deixar buraco
                boundary = (a["t_last"] + b["t_first"]) / 2
            a["t_last"] = b["t_first"] = boundary

        for i, s in enumerate(segments):
            flag = "" if s["reliable"] else "  <-- sem confirmação suficiente, mantendo áudio original da câmera aqui"
            print(f"  [{s['t_first']:7.2f} - {s['t_last']:7.2f}] offset={s['offset']:+7.2f}s "
                  f"conf={s['confidence']:.2f} ({s['n_probes']} sondagens){flag}")
        offsets = [s["offset"] for s in segments if s["reliable"]]
        if any(b < a - OFFSET_TOL for a, b in zip(offsets, offsets[1:])):
            print("aviso: a ordem dos trechos confiáveis na gravação externa não é crescente — confira se não "
                  "há pedaços fora de ordem ou de outra gravação")

        # áudio nativo da própria câmera, pra usar nos trechos sem casamento confiável
        cam_native_wav = tmp / "cam_native.wav"
        ffmpeg("-i", str(args.video), "-vn", str(cam_native_wav))
        cam_native, cam_native_sr = sf.read(cam_native_wav, always_2d=True)

        # monta o áudio final a partir da gravação externa em qualidade nativa (não os 22050 Hz da análise)
        raw_native, raw_sr = sf.read(raw_native_wav, always_2d=True)
        n_ch = raw_native.shape[1]
        out = np.zeros((0, n_ch), dtype=raw_native.dtype)
        for s in segments:
            if s["reliable"]:
                start = int(round((s["t_first"] + s["offset"]) * raw_sr))
                end = start + int(round((s["t_last"] - s["t_first"]) * raw_sr))
                start, end = max(0, start), min(len(raw_native), end)
                piece = raw_native[start:end]
            else:
                start = int(round(s["t_first"] * cam_native_sr))
                end = int(round(s["t_last"] * cam_native_sr))
                piece = cam_native[start:end]
                if cam_native_sr != raw_sr:
                    piece = librosa.resample(piece.T.astype(np.float64), orig_sr=cam_native_sr, target_sr=raw_sr).T
                if piece.shape[1] != n_ch:
                    piece = np.repeat(piece.mean(axis=1, keepdims=True), n_ch, axis=1) if piece.shape[1] > n_ch \
                        else np.repeat(piece, n_ch, axis=1)
                piece = piece.astype(raw_native.dtype)
            out = crossfade_append(out, piece, raw_sr)

        target_len = int(round(video_dur * raw_sr))
        if len(out) < target_len:
            out = np.concatenate([out, np.zeros((target_len - len(out), out.shape[1]), dtype=out.dtype)])
        else:
            out = out[:target_len]
        sf.write(out_dir / "audio.wav", out, raw_sr, subtype="PCM_24")

    vf = ["-vf", COLOR_GRADE] if args.grade else []
    ffmpeg("-i", str(args.video), "-an", *vf, "-c:v", "libx264", "-preset", "medium",
           "-crf", "16", "-pix_fmt", "yuv420p", str(out_dir / "video.tmp.mp4"))
    replace_with_retry(out_dir / "video.tmp.mp4", out_dir / "video.mp4")

    report = {
        "source": {"video": str(args.video), "rawAudio": str(args.raw_audio),
                   "videoDuration": r(video_dur), "rawAudioDuration": r(len(line) / SR)},
        "segments": [{"start": r(s["t_first"]), "end": r(s["t_last"]), "offset": r(s["offset"]),
                      "confidence": s["confidence"], "nProbes": s["n_probes"],
                      "source": "raw_mic" if s["reliable"] else "camera_fallback"} for s in segments],
    }
    (out_dir / "resync.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
