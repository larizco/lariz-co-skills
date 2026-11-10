"""Cria <projeto>/carrosseis/<slug>/_src/ com base.css, tokens.css, fontes e elementos da marca.

Uso:  python new_carousel.py <projeto> "titulo do carrossel"
Pré-requisito: <projeto>/marca/tokens.json (rode `marca.py init` / o passo de marca da skill).
Depois copie para _src/img/ só os assets extras que for usar (prints, fotos).
"""
import re
import shutil
import sys
import unicodedata
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).parent))
from marca import cmd_css  # noqa: E402


def slug(t: str) -> str:
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def main() -> None:
    proj = Path(sys.argv[1]).resolve()
    marca = proj / "marca"
    if not (marca / "tokens.json").exists():
        sys.exit("sem marca/tokens.json: faça o passo de marca primeiro")
    cmd_css(proj)
    folder = proj / "carrosseis" / slug(sys.argv[2])
    n = 2
    while folder.exists():  # nunca sobrescreve um carrossel anterior
        folder = folder.with_name(f"{slug(sys.argv[2])}-{n}")
        n += 1
    src = folder / "_src"
    (src / "img").mkdir(parents=True)
    shutil.copy(SKILL / "assets" / "base.css", src / "base.css")
    shutil.copy(marca / "tokens.css", src / "tokens.css")
    shutil.copytree(marca / "fontes", src / "fontes", dirs_exist_ok=True)
    if (marca / "elementos").exists():
        shutil.copytree(marca / "elementos", src / "img" / "elementos", dirs_exist_ok=True)
    print(folder)


if __name__ == "__main__":
    main()
