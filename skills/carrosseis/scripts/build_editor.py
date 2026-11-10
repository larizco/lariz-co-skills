"""Gera o editor visual (artefato) de um carrossel: slides embutidos + comentar/arrastar/redimensionar/girar.

Uso:  python build_editor.py <projeto>/carrosseis/<slug>
Saída: <slug>/_editor.html  (publicar com a ferramenta Artifact; capabilities {db:{}})
Imagens e fontes viram data URIs (PNG -> WebP) para o artefato ser autossuficiente.
"""
import base64
import io
import json
import re
import sys
from pathlib import Path

from PIL import Image

SKILL = Path(__file__).resolve().parents[1]
folder = Path(sys.argv[1]).resolve()
src = folder / "_src"
proj = folder.parents[1]
cache: dict[str, str] = {}
MIME = {".webp": "image/webp", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".svg": "image/svg+xml", ".gif": "image/gif"}
FONT_MIME = {".woff2": ("font/woff2", "woff2"), ".woff": ("font/woff", "woff"), ".otf": ("font/otf", "opentype"), ".ttf": ("font/ttf", "truetype")}


def data_uri(name: str) -> str:
    if name in cache:
        return cache[name]
    p = src / "img" / name
    if p.suffix.lower() == ".png":
        im = Image.open(p)
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=88, method=4)
        mime, raw = "image/webp", buf.getvalue()
    else:
        mime, raw = MIME[p.suffix.lower()], p.read_bytes()
    cache[name] = f"data:{mime};base64,{base64.b64encode(raw).decode()}"
    return cache[name]


def embed(text: str, in_html: bool) -> str:
    if in_html:  # <img src="img/x.png"> -> src=data + data-orig
        text = re.sub(r'src="img/([^"]+)"', lambda m: f'data-orig="{m.group(1)}" src="{data_uri(m.group(1))}"', text)
    return re.sub(r'url\((["\']?)img/([^)"\']+)\1\)', lambda m: f'url("{data_uri(m.group(2))}")', text)


tokens = json.loads((proj / "marca" / "tokens.json").read_text(encoding="utf-8"))
faces = []
for role in ("display", "body", "script"):
    f = tokens["fonts"].get(role)
    for fl in (f or {}).get("files", []):
        p = src / "fontes" / fl["file"]
        mime, fmt = FONT_MIME.get(p.suffix.lower(), ("font/woff2", "woff2"))
        b64 = base64.b64encode(p.read_bytes()).decode()
        faces.append(f'@font-face{{font-family:"{f["family"]}";src:url(data:{mime};base64,{b64}) format("{fmt}");font-weight:{fl.get("weight", "400")}}}')

css_tokens = re.sub(r"@font-face\{[^}]*\}", "", (src / "tokens.css").read_text(encoding="utf-8"))
base = css_tokens + "\n" + (src / "base.css").read_text(encoding="utf-8")
slides = []
for f in sorted(src.glob("[0-9][0-9]-*.html")):
    t = f.read_text(encoding="utf-8")
    css = "\n".join(re.findall(r"<style>(.*?)</style>", t, re.S))
    body = re.search(r"<body[^>]*>(.*)</body>", t, re.S).group(1)
    slides.append({"n": int(f.name[:2]), "name": f.stem[3:], "css": embed(css, False), "html": embed(body, True)})

disp = tokens["fonts"].get("display")
display_stack = f'"{disp["family"]}",serif' if disp else "serif"
data = {"title": folder.name, "base": embed(base, False), "slides": slides}
out = (SKILL / "assets" / "editor" / "template.html").read_text(encoding="utf-8")
out = out.replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", r"<\/"))
out = out.replace("__FONTFACES__", "\n".join(faces)).replace("__DISPLAY__", display_stack)
dest = folder / "_editor.html"
dest.write_text(out, encoding="utf-8")
print(dest, f"{dest.stat().st_size / 1e6:.1f} MB")
