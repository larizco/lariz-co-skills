"""Prepara <projeto>/reels/ a partir do template da skill (Remotion + pipeline Python). Idempotente.

Uso: python setup_reels.py <projeto> [--check]
  - copia template/ -> <projeto>/reels/ sem sobrescrever o que já existe (src/brand.ts é regerado pela marca)
  - cria reels/prontos/ e reels/prontos/capas/
  - se existir <projeto>/marca/tokens.json, roda `marca.py ts` (brand.ts + public/marca/)
  - --check: só diz o que falta instalar (node, npm, ffmpeg, python 3.11, uv, .venv, node_modules)
"""
import shutil
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).parent))


def check(reels: Path) -> None:
    def has(cmd: str) -> str:
        return "ok" if shutil.which(cmd) else "FALTA"

    venv_py = reels / "pipeline" / ".venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    rows = [
        ("node", has("node")), ("npm", has("npm")), ("ffmpeg", has("ffmpeg")), ("uv", has("uv")),
        ("reels/remotion/node_modules", "ok" if (reels / "remotion" / "node_modules").exists() else "FALTA (npm install)"),
        ("reels/pipeline/.venv", "ok" if venv_py.exists() else "FALTA (ver SKILL.md, passo 2)"),
    ]
    for k, v in rows:
        print(f"  {k:32} {v}")


def main() -> None:
    proj = Path(sys.argv[1]).resolve()
    reels = proj / "reels"
    if "--check" in sys.argv:
        check(reels)
        return
    for src in (SKILL / "template").rglob("*"):
        if src.is_dir() or "__pycache__" in src.parts:
            continue
        dst = reels / src.relative_to(SKILL / "template")
        if dst.exists():
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    (reels / "prontos" / "capas").mkdir(parents=True, exist_ok=True)
    (reels / "remotion" / "public" / "videos").mkdir(parents=True, exist_ok=True)
    if (proj / "marca" / "tokens.json").exists():
        from marca import cmd_ts

        cmd_ts(proj)
    print(reels)
    check(reels)


if __name__ == "__main__":
    main()
