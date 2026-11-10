"""Kit de marca compartilhado das skills lariz.co (reels + carrosséis). Criado por Lariz · lariz.co.

A marca mora em <projeto>/marca/ e é a MESMA pros vídeos e pros carrosséis:
  marca/marca.md        voz, público, regras (texto pra ler antes de criar)
  marca/tokens.json     cores, fontes, logo, CTA (fonte da verdade pros scripts)
  marca/tokens.css      gerado: variáveis CSS + @font-face (carrosséis)
  marca/fontes/         arquivos de fonte
  marca/elementos/      SVG/PNG reutilizáveis + README.md (índice)
  marca/referencias/    prints, inspirações, posts antigos que a pessoa curte

Uso:
  python marca.py init  <projeto> [--nome "Minha Marca"]
  python marca.py fonte <projeto> "<Família do Google Fonts>" --papel display|body|script [--pesos 400,700]
  python marca.py css   <projeto>                 -> marca/tokens.css
  python marca.py ts    <projeto>                 -> reels/remotion/src/brand.ts + public/marca/ (fontes, elementos, logo)
  python marca.py board <projeto>                 -> marca/board.html (+ board.png se achar Chrome/Edge) pra aprovação
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
FALLBACK = {"display": "serif", "body": "system-ui, sans-serif", "script": "cursive"}

DEFAULT_TOKENS = {
    "name": "Minha Marca",
    "handle": "@minhamarca",
    "lang": "pt",
    "colors": {
        "ink": "#2B2B2B",
        "paper": "#FFFFFF",
        "accent": "#E4572E",
        "accent2": "#F2C14E",
        "soft": ["#FDF0E6", "#E8F1EC", "#EDE7F6"],
        "muted": "#6B6B6B",
        "border": "#E6E1DC",
        "success": "#2E7D5B",
    },
    "fonts": {"display": None, "body": None, "script": None},
    "caption": {"color": "#FFFFFF", "weight": 800, "keywordColor": "#FFFFFF"},
    "logo": None,
    "cta": {"text": "link na bio", "button": "quero!", "buttonDone": "pronto ✨"},
}


def chrome() -> str | None:
    for p in [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ]:
        if Path(p).exists():
            return p
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome", "msedge"):
        if shutil.which(name):
            return shutil.which(name)
    return None


def load(proj: Path) -> dict:
    f = proj / "marca" / "tokens.json"
    if not f.exists():
        sys.exit(f"não achei {f} — rode `marca.py init {proj}` primeiro")
    return json.loads(f.read_text(encoding="utf-8"))


def save(proj: Path, tokens: dict) -> None:
    (proj / "marca" / "tokens.json").write_text(json.dumps(tokens, indent=2, ensure_ascii=False), encoding="utf-8")


def font_stack(tokens: dict, role: str) -> str:
    f = tokens["fonts"].get(role)
    if not f and role == "script":  # sem manuscrita: usa a display
        f = tokens["fonts"].get("display")
    if not f:
        return FALLBACK[role]
    return f"'{f['family']}', {f.get('fallback', FALLBACK[role])}"


def cmd_init(proj: Path, nome: str | None) -> None:
    m = proj / "marca"
    for d in ("fontes", "elementos", "referencias"):
        (m / d).mkdir(parents=True, exist_ok=True)
    if not (m / "tokens.json").exists():
        t = json.loads(json.dumps(DEFAULT_TOKENS))
        if nome:
            t["name"] = nome
        save(proj, t)
    idx = m / "elementos" / "README.md"
    if not idx.exists():
        idx.write_text("# Elementos da marca\n\nUm por linha: `arquivo` — o que é — quando usar.\n\n", encoding="utf-8")
    print(m)


def cmd_fonte(proj: Path, family: str, papel: str, pesos: str) -> None:
    tokens = load(proj)
    out_dir = proj / "marca" / "fontes"
    out_dir.mkdir(parents=True, exist_ok=True)
    files = []
    for w in [p.strip() for p in pesos.split(",") if p.strip()]:
        url = f"https://fonts.googleapis.com/css2?family={family.replace(' ', '+')}:wght@{w}&display=swap"
        try:
            css = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read().decode()
        except Exception as e:  # peso que a família não tem, nome errado...
            print(f"  ! {family} {w}: {e}")
            continue
        # pega o bloco /* latin */ (cobre acentos do português); senão, o último src
        m = re.search(r"/\* latin \*/\s*@font-face\s*{[^}]*?url\((https://[^)]+)\)", css) or list(re.finditer(r"url\((https://[^)]+)\)", css))[-1]
        src = m.group(1)
        ext = Path(src.split("?")[0]).suffix or ".woff2"
        name = f"{family.replace(' ', '')}-{w}{ext}"
        urllib.request.urlretrieve(src, out_dir / name)
        files.append({"file": name, "weight": w})
        print(f"  {name}")
    if not files:
        sys.exit("nenhum arquivo baixado: confira o nome exato em fonts.google.com")
    tokens["fonts"][papel] = {"family": family, "files": files, "fallback": FALLBACK[papel]}
    save(proj, tokens)


def cmd_css(proj: Path) -> Path:
    t = load(proj)
    faces = []
    for role in ("display", "body", "script"):
        f = t["fonts"].get(role)
        if not f:
            continue
        for fl in f["files"]:
            fmt = {".woff2": "woff2", ".woff": "woff", ".otf": "opentype", ".ttf": "truetype"}.get(Path(fl["file"]).suffix.lower(), "woff2")
            faces.append(f'@font-face{{font-family:"{f["family"]}";src:url(fontes/{fl["file"]}) format("{fmt}");font-weight:{fl.get("weight", "400")}}}')
    c = t["colors"]
    soft = c["soft"] + [c["paper"]] * (3 - len(c["soft"]))
    css = "\n".join(faces) + f"""
:root{{
  --ink:{c['ink']}; --paper:{c['paper']}; --accent:{c['accent']}; --accent2:{c['accent2']};
  --soft1:{soft[0]}; --soft2:{soft[1]}; --soft3:{soft[2]};
  --muted:{c['muted']}; --border:{c['border']}; --success:{c['success']};
  --font-display:{font_stack(t, 'display')}; --font-body:{font_stack(t, 'body')}; --font-script:{font_stack(t, 'script')};
}}
"""
    out = proj / "marca" / "tokens.css"
    out.write_text(css, encoding="utf-8")
    print(out)
    return out


def cmd_ts(proj: Path) -> None:
    t = load(proj)
    remotion = proj / "reels" / "remotion"
    if not (remotion / "src").exists():
        sys.exit(f"não achei {remotion}/src — copie o template da skill de reels primeiro")
    pub = remotion / "public" / "marca"
    for d in ("fontes", "elementos"):
        src = proj / "marca" / d
        if src.exists():
            shutil.copytree(src, pub / d, dirs_exist_ok=True)
    logo = None
    if t.get("logo"):
        lp = proj / "marca" / t["logo"]
        if lp.exists():
            shutil.copy(lp, pub / lp.name)
            logo = f"marca/{lp.name}"
    font_files = [
        {"family": f["family"], "file": fl["file"], "weight": str(fl.get("weight", "400"))}
        for role in ("display", "body", "script")
        if (f := t["fonts"].get(role))
        for fl in f["files"]
    ]
    c = t["colors"]
    brand = {
        "name": t["name"],
        "handle": t.get("handle", ""),
        "colors": c,
        "fonts": {r: font_stack(t, r) for r in ("display", "body", "script")},
        "fontFiles": font_files,
        "caption": t.get("caption", DEFAULT_TOKENS["caption"]),
        "logo": logo,
        "cta": t.get("cta", DEFAULT_TOKENS["cta"]),
    }
    body = json.dumps(brand, indent=2, ensure_ascii=False)
    ts = (
        "// ARQUIVO GERADO por `python marca.py ts <projeto>` a partir de <projeto>/marca/tokens.json.\n"
        "// Não edite à mão: mude o tokens.json e gere de novo.\n"
        f"export const BRAND = {body} as {{\n"
        "  name: string; handle: string;\n"
        "  colors: { ink: string; paper: string; accent: string; accent2: string; soft: string[]; muted: string; border: string; success: string };\n"
        "  fonts: { display: string; body: string; script: string };\n"
        "  fontFiles: { family: string; file: string; weight?: string }[];\n"
        "  caption: { color: string; weight: number; keywordColor: string };\n"
        "  logo: string | null;\n"
        "  cta: { text: string; button: string; buttonDone: string };\n"
        "};\n"
    )
    (remotion / "src" / "brand.ts").write_text(ts, encoding="utf-8")
    print(remotion / "src" / "brand.ts")


def cmd_board(proj: Path) -> None:
    t = load(proj)
    cmd_css(proj)
    m = proj / "marca"
    c = t["colors"]
    sw = [("ink", c["ink"]), ("paper", c["paper"]), ("accent", c["accent"]), ("accent2", c["accent2"])]
    sw += [(f"soft{i + 1}", v) for i, v in enumerate(c["soft"])]
    sw += [("muted", c["muted"]), ("success", c["success"])]
    els = sorted(p for p in (m / "elementos").glob("*") if p.suffix.lower() in (".svg", ".png", ".webp", ".jpg"))
    logo = f'<img src="{t["logo"]}" style="height:120px">' if t.get("logo") else ""
    html = f"""<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="tokens.css">
<style>*{{box-sizing:border-box;margin:0}}body{{width:1600px;padding:60px;background:var(--paper);color:var(--ink);font-family:var(--font-body)}}
h1{{font-family:var(--font-display);font-size:96px;line-height:1}}h2{{font:700 22px var(--font-body);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:48px 0 18px}}
.sw{{display:flex;gap:16px;flex-wrap:wrap}}.sw div{{width:150px}}.sw i{{display:block;height:110px;border-radius:22px;border:2px solid var(--border)}}.sw b{{display:block;font-size:18px;margin-top:8px}}.sw span{{font-size:16px;color:var(--muted)}}
.ty p{{margin-bottom:14px}}.el{{display:flex;gap:28px;flex-wrap:wrap;align-items:center}}.el figure{{width:170px;text-align:center;font-size:14px;color:var(--muted)}}.el img{{width:150px;height:150px;object-fit:contain;background:var(--soft1);border-radius:20px;padding:12px}}</style>
<div style="display:flex;justify-content:space-between;align-items:center"><h1>{t['name']}</h1>{logo}</div>
<p style="font-size:26px;margin-top:10px">{t.get('handle', '')}</p>
<h2>cores</h2><div class="sw">{''.join(f'<div><i style="background:{v}"></i><b>{k}</b><span>{v}</span></div>' for k, v in sw)}</div>
<h2>tipografia</h2><div class="ty">
<p style="font-family:var(--font-display);font-size:110px;line-height:1">título grande de gancho</p>
<p style="font-size:40px">texto de apoio leve com uma <b>palavra forte</b> no meio — áéíóú ãõ ç</p>
<p style="font-family:var(--font-script);font-size:64px;color:var(--accent)">comentário manuscrito ✨</p>
<p><span style="background:var(--accent);color:#fff;padding:10px 26px;border-radius:999px;font-weight:700;font-size:28px">botão / etiqueta</span>
<span style="background:var(--soft1);padding:10px 26px;border-radius:999px;font-size:28px;margin-left:10px">chip suave</span></p></div>
<h2>elementos ({len(els)})</h2><div class="el">{''.join(f'<figure><img src="elementos/{p.name}"><figcaption>{p.stem}</figcaption></figure>' for p in els) or '<p>nenhum ainda</p>'}</div>
"""
    out = m / "board.html"
    out.write_text(html, encoding="utf-8")
    print(out)
    ch = chrome()
    if ch:
        png = m / "board.png"
        subprocess.run([ch, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1600,1700",
                        "--virtual-time-budget=4000", f"--screenshot={png}", out.resolve().as_uri()], check=False, capture_output=True)
        if png.exists():
            print(png)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["init", "fonte", "css", "ts", "board"])
    ap.add_argument("projeto", type=Path)
    ap.add_argument("family", nargs="?")
    ap.add_argument("--nome")
    ap.add_argument("--papel", choices=["display", "body", "script"])
    ap.add_argument("--pesos", default="400,700")
    a = ap.parse_args()
    proj = a.projeto.resolve()
    if a.cmd == "init":
        cmd_init(proj, a.nome)
    elif a.cmd == "fonte":
        if not a.family or not a.papel:
            sys.exit('uso: marca.py fonte <projeto> "Família" --papel display|body|script')
        cmd_fonte(proj, a.family, a.papel, a.pesos)
    elif a.cmd == "css":
        cmd_css(proj)
    elif a.cmd == "ts":
        cmd_ts(proj)
    else:
        cmd_board(proj)


if __name__ == "__main__":
    main()
