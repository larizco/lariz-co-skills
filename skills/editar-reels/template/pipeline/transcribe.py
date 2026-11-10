"""Transcreve remotion/public/videos/<slug>/audio.wav com tempo de cada palavra (WhisperX).

Uso: python transcribe.py <slug> [--whisper large-v3-turbo] [--lang pt] [--prompt "nome da marca, termos do tema"]
Saída em remotion/public/videos/<slug>/: transcript.json {lines, words}
"""
import argparse
import json
from pathlib import Path

from common import VIDEOS_DIR, ensure_ffmpeg_on_path


def r(x, nd=3):
    return round(float(x), nd)


def transcribe(audio: Path, model_name: str, prompt: str, lang: str):
    ensure_ffmpeg_on_path()
    import whisperx

    wav = whisperx.load_audio(str(audio))
    try:
        model = whisperx.load_model(model_name, device="cpu", compute_type="int8", language=lang,
                                    asr_options={"initial_prompt": prompt}, vad_method="silero")
    except TypeError:
        model = whisperx.load_model(model_name, device="cpu", compute_type="int8", language=lang,
                                    asr_options={"initial_prompt": prompt})
    result = model.transcribe(wav, batch_size=8, language=lang)
    align_model, meta = whisperx.load_align_model(language_code=lang, device="cpu")
    aligned = whisperx.align(result["segments"], align_model, meta, wav, "cpu", return_char_alignments=False)

    words, lines = [], []
    for seg in aligned["segments"]:
        seg_words = [w for w in seg.get("words", []) if "start" in w]
        if not seg_words:
            continue
        lines.append({"text": seg["text"].strip(), "start": r(seg_words[0]["start"]), "end": r(seg_words[-1]["end"])})
        for w in seg_words:
            words.append({"word": w["word"].strip(), "start": r(w["start"]), "end": r(w["end"]),
                          "score": r(w.get("score", 0), 2)})
    return words, lines


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--whisper", default="large-v3-turbo")
    ap.add_argument("--prompt", default="", help="nomes próprios e termos do tema (ajuda o Whisper a escrever certo)")
    ap.add_argument("--lang", default="pt")
    args = ap.parse_args()

    video_dir = VIDEOS_DIR / args.slug
    audio = video_dir / "audio.wav"
    print(f"transcrevendo {audio} (whisperx {args.whisper})...")
    words, lines = transcribe(audio, args.whisper, args.prompt, args.lang)

    out = {"lines": lines, "words": words}
    (video_dir / "transcript.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{len(lines)} frases, {len(words)} palavras")
    for ln in lines:
        print(f"  [{ln['start']:7.2f} - {ln['end']:7.2f}] {ln['text']}")


if __name__ == "__main__":
    main()
