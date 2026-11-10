"""Renderiza os slides HTML de um carrossel para PNG via Chrome headless.

Uso:  python render.py <pasta-do-carrossel> [--preview] [--scale N] [slide.html ...]
  final (só depois da aprovação):  <pasta>/_src/NN-nome.html -> <pasta>/NN-nome.png  em 2160x2700 (escala 2, nítido)
  --preview: confere o visual para você mesma -> <pasta>/_src/_preview/NN-nome.png (escala 1; NÃO é entrega)
Slide com <meta name="transparent"> sai com fundo transparente (para encaixar foto depois).
"""
import subprocess, sys, re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from marca import chrome  # noqa: E402

CHROME = chrome()
if not CHROME:
    sys.exit("não achei Chrome/Edge/Chromium: instale um deles para renderizar os slides")

def render(html: Path, out: Path, scale: int):
    transparent = 'name="transparent"' in html.read_text(encoding="utf-8")
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
           f"--force-device-scale-factor={scale}", "--window-size=1080,1350",
           "--virtual-time-budget=4000", f"--screenshot={out}"]
    if transparent:
        cmd.append("--default-background-color=00000000")
    cmd.append(html.resolve().as_uri())
    subprocess.run(cmd, check=True, capture_output=True)
    return transparent

def main():
    args = sys.argv[1:]
    preview = "--preview" in args
    if preview: args.remove("--preview")
    scale = 1 if preview else 2
    if "--scale" in args:
        i = args.index("--scale"); scale = int(args[i + 1]); del args[i:i + 2]
    folder = Path(args[0]).resolve(); src = folder / "_src"
    outdir = src / "_preview" if preview else folder
    outdir.mkdir(exist_ok=True)
    files = [src / f for f in args[1:]] or sorted(src.glob("[0-9][0-9]-*.html"))
    for f in files:
        out = outdir / (f.stem + ".png")
        t = render(f, out, scale)
        print(("[transparente] " if t else "") + out.name)

if __name__ == "__main__":
    main()
