"""Developer tasks exposed as ``[project.scripts]`` entry points.

Run via uv, e.g. ``uv run babel-extract`` / ``uv run babel-init en`` /
``uv run babel-compile``. Kept free of app imports so the commands do not load
config, .env, or the database.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_TEXTS = ROOT / "zmanim_bot" / "texts"
_LOCALES = ROOT / "locales"
_POT = _LOCALES / "zmanim_bot.pot"
# `plural/units.py` holds the plural msgids (year/years, minute/minutes, …) that
# the runtime uses via `_(*units.tu_*, n)`; it must be extracted too, or the .pot
# loses every msgid_plural entry.
_EXTRACT_SOURCES = [
    _TEXTS / "plural" / "units.py",
    _TEXTS / "single" / "buttons.py",
    _TEXTS / "single" / "headers.py",
    _TEXTS / "single" / "helpers.py",
    _TEXTS / "single" / "messages.py",
    _TEXTS / "single" / "names.py",
    _TEXTS / "single" / "zmanim.py",
]


def _run(args: list[str]) -> None:
    raise SystemExit(subprocess.run(args, cwd=ROOT).returncode)


def babel_extract() -> None:
    _run([
        "pybabel", "extract", *map(str, _EXTRACT_SOURCES),
        "-o", str(_POT), "-k", "__:1,2", "--add-comments=NOTE",
    ])


def babel_init() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: uv run babel-init <language-code>")
    _run([
        "pybabel", "init", "-i", str(_POT),
        "-d", str(_LOCALES), "-D", "zmanim_bot", "-l", sys.argv[1],
    ])


def babel_compile() -> None:
    _run(["pybabel", "compile", "-d", str(_LOCALES), "-D", "zmanim_bot"])
