"""MODELO de script de cenas. Copie pra public/videos/<slug>/build.py e adapte.

Gera o edit-plan.json inteiro (idempotente): cenas escritas aqui + legendas/palavras-chave automáticas a partir do
transcript.json. Todos os tempos em SEGUNDOS do vídeo final (mesma base do transcript), inclusive os de dentro das
props (`at`, `doneAt`, `tapAt`...). Rodar de dentro da pasta do vídeo:  <PY> build.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[3] / "pipeline"))
from captions import build, load_words  # noqa: E402

SLUG = HERE.name
FORMAT = "vertical"  # ou "horizontal"
words = load_words(HERE / "transcript.json")
END = round(words[-1]["end"] + 0.6, 2)  # ou a duração exata do video.mp4

# ── gancho: título gigante (cada linha pula na palavra) + um card que já "vive" a frase ──
hook = [
    dict(id="hook-title", type="HookTitle", start=0, end=4.2, props=dict(lines=[
        dict(text="3 erros", at=0.2), dict(text="que travam", at=0.7), dict(text="seu perfil", at=1.1)])),
    dict(id="hook-card", type="Notification", start=0, end=4.2, layout=dict(x=830, y=560, scale=0.6), props=dict(
        items=[dict(title="0 curtidas", text="no post de ontem", at=0.3, emoji="💔"),
               dict(title="1 novo seguidor", text="(era sua mãe)", at=0.8, emoji="🙃")],
        shakeAt=1.3)),
]

# ── miolo: um card por bloco de assunto, trocando junto com a fala ──
scenes = [
    dict(id="erros", type="ListCard", start=4.2, end=12.0, layout=dict(y=600, scale=1.15), props=dict(
        title="os 3 erros", numbered=True,
        items=[dict(text="gancho fraco", at=4.6, strikeAt=9.0),
               dict(text="legenda gigante", at=6.0, strikeAt=9.4),
               dict(text="sem chamada", at=7.4, strikeAt=9.8)],
        stamp=dict(text="dá pra mudar!", at=10.5))),
    dict(id="resultado", type="BigNumber", start=12.0, end=17.0, layout=dict(y=600, scale=1.15), props=dict(
        label="alcance depois de ajustar", steps=[dict(at=12.3, v=0), dict(at=13.4, v=48)], suffix="k",
        max=60, caption="em 30 dias")),
]

# ── fecho: recap + CTA ──
outro = [
    dict(id="recap", type="Recap", start=17.0, end=21.0, layout=dict(y=600, scale=1.2), props=dict(
        title="nesse vídeo:", items=[dict(text="gancho forte", at=17.4), dict(text="legenda curta", at=18.0),
                                     dict(text="CTA claro", at=18.6)])),
    dict(id="cta", type="CTA", start=21.0, end=END, layout=dict(y=600, scale=1.3), props=dict(
        tapAt=21.6, doneAt=22.6, bioAt=23.0, subtitle="conteúdo toda semana")),
]

# palavras-chave: (palavra exatamente como no transcript, tempo aproximado) → saem SOZINHAS, gigantes
KEYWORDS = [("gancho", 5.0), ("alcance", 12.5)]

# legendas começam depois do gancho (o título gigante já é o texto ali) e nunca durante a apresentação do nome
captions = build(words, 4.2, END, KEYWORDS)

plan = dict(
    slug=SLUG, title=SLUG, format=FORMAT, trim=dict(start=0, end=END),
    media=dict(video="video.mp4", audio="audio.wav"),
    events=hook + scenes + outro + captions,
)
(HERE / "edit-plan.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{len(plan['events'])} eventos ({len(captions)} legendas/palavras-chave) -> edit-plan.json")
