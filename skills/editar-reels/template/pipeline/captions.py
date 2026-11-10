"""Gera eventos Caption/Keyword curtinhos a partir do transcript.json (padrão lariz.co: legendas curtinhas).

Regras: no máximo 4 palavras / 1.6s por legenda, quebra em pontuação e pausas; palavra-chave sai SOZINHA
como evento Keyword (nunca misturada na legenda).

Uso como módulo: build(words, start, end, keywords) -> lista de eventos.
Uso CLI:  python captions.py <transcript.json> <start> <end> --kw propósito@59 realização ...
"""
import argparse
import json
import re
import unicodedata

MAX_WORDS = 4
MAX_DUR = 1.6
GAP = 0.25
KW_MIN = 1.1


def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def load_words(path):
    d = json.load(open(path, encoding="utf-8"))
    return d.get("words") or [w for s in d["segments"] for w in s.get("words", [])]


def build(words, start, end, keywords):
    """keywords: lista de (palavra, tempo_aproximado) — casa a ocorrência mais próxima do tempo."""
    # palavras "esticadas" pelo Whisper (pausa no meio da fala) faziam a legenda parecer travada
    ws = [{**w, "end": min(w["end"], w["start"] + 0.55)} for w in words if start <= w["start"] < end]
    kw_idx = set()
    for k, approx in keywords:
        cands = [i for i, w in enumerate(ws) if norm(w["word"]) == norm(k)]
        if cands:
            kw_idx.add(min(cands, key=lambda i: abs(ws[i]["start"] - approx)))

    events, chunk = [], []

    def flush(next_start):
        if not chunk:
            return
        text = " ".join(w["word"] for w in chunk).strip()
        s = chunk[0]["start"]
        e = min(next_start, chunk[-1]["end"] + 0.3) if next_start else chunk[-1]["end"] + 0.3
        events.append({"type": "Caption", "start": round(s, 3), "end": round(max(e, s + 0.4), 3), "props": {"text": text}})
        chunk.clear()

    for i, w in enumerate(ws):
        nxt = ws[i + 1]["start"] if i + 1 < len(ws) else end
        if i in kw_idx:
            flush(w["start"])
            word = re.sub(r"[.,!?…]+$", "", w["word"])
            e = max(w["end"] + 0.25, w["start"] + KW_MIN)
            events.append({"type": "Keyword", "start": round(w["start"], 3), "end": round(e, 3), "props": {"text": word}})
            continue
        if events and events[-1]["type"] == "Keyword" and w["start"] < events[-1]["end"] and not chunk:
            w = {**w, "start": events[-1]["end"]}
        chunk.append(w)
        dur = w["end"] - chunk[0]["start"]
        punct = re.search(r"[.,!?…]$", w["word"])
        if len(chunk) >= MAX_WORDS or dur >= MAX_DUR or punct or nxt - w["end"] > GAP or (i + 1) in kw_idx:
            flush(nxt)
    flush(None)
    for prev, cur in zip(events, events[1:]):  # nunca duas legendas ao mesmo tempo
        if cur["start"] < prev["end"]:
            if prev["type"] == "Keyword":  # palavra-chave fica o tempo todo; a legenda seguinte espera
                cur["start"] = prev["end"]
                cur["end"] = max(cur["end"], round(cur["start"] + 0.4, 3))
            elif cur["type"] == "Keyword":  # a palavra-chave entra na hora certa; a legenda anterior sai
                prev["end"] = cur["start"]
            else:
                prev["end"] = round(max(prev["start"] + 0.3, cur["start"]), 3)
                cur["start"] = max(cur["start"], prev["end"])
    events = [e for e in events if e["end"] - e["start"] >= 0.15]
    for n, ev in enumerate(events):
        ev["id"] = f"{'kw' if ev['type'] == 'Keyword' else 'cap'}-{ev['start']:.2f}"
    return events


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("transcript")
    ap.add_argument("start", type=float)
    ap.add_argument("end", type=float)
    ap.add_argument("--kw", nargs="*", default=[], help="palavra@tempo")
    a = ap.parse_args()
    kws = [(k.split("@")[0], float(k.split("@")[1])) for k in a.kw]
    print(json.dumps(build(load_words(a.transcript), a.start, a.end, kws), ensure_ascii=False, indent=1))
