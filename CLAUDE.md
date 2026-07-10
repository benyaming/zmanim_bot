# CLAUDE.md

Guidance for working in this repository.

## What this is

A Telegram bot ([@zmanim_bot](https://t.me/zmanim_bot)) that reports Jewish
prayer/observance times (zmanim, Shabbat, holidays, daf yomi, etc.) and renders
them as images. Built on **aiogram 2.24** (async, long-polling in dev / webhook
in prod). Localized in English, Russian, and Hebrew.

## Toolchain: uv

This project uses **uv** (migrated from pdm). Python is pinned to **3.10.7**
(`.python-version`, `requires-python`); uv fetches a managed CPython if the host
lacks it. All dependencies are pinned to exact versions in `pyproject.toml`; the
resolved set is committed in `uv.lock`.

- Install / update env: `uv sync`
- Add or change a dependency: edit `pyproject.toml`, then `uv lock` and `uv sync`
- Dev tasks are `[project.scripts]` entry points (the uv-standard way; requires
  the hatchling build-system that's configured here):
  - `uv run babel-extract` — extract translatable strings from `texts/single/*` → `locales/zmanim_bot.pot`
  - `uv run babel-init <lang>` — initialize a new locale
  - `uv run babel-compile` — compile `.po` → `.mo`
  - Implementations live in `zmanim_bot/tasks.py`.

## Running locally

The bot polls (not webhook) unless `IS_PROD` is set. Config comes from `.env`
(pydantic `BaseSettings`, resolved relative to the CWD — run from the repo root).

Prerequisites:
- **MongoDB** on `localhost:27017` and **Redis** on `localhost:6379` (both run
  as docker containers here; `mongo:6`, `redis:7`). `DB_URL` unset ⇒ localhost.
- `.env` active `BOT_TOKEN` is the **dev** bot `@benyomintestbot` (the prod token
  is commented out) — safe to run locally.

Run:

```bash
PYTHONPATH=. .venv/bin/python zmanim_bot/main.py
```

### macOS image-rendering gotcha (libraqm)

`renderer._draw_line` always passes `direction=` to `ImageDraw.text`, which
requires **libraqm**. The macOS PyPI Pillow wheel is built WITHOUT raqm
(`PIL.features.check('raqm')` → False), so any image render raises
`KeyError: '... not supported without libraqm'`. Fix locally by building Pillow
from source against Homebrew's libraqm:

```bash
brew install libraqm
PKG_CONFIG_PATH=/opt/homebrew/lib/pkgconfig CFLAGS=-I/opt/homebrew/include \
  LDFLAGS=-L/opt/homebrew/lib \
  uv pip install --no-binary pillow --reinstall-package pillow pillow==11.0.0
```

Re-running a plain `uv sync` reverts to the raqm-less wheel — re-run the above if
so, or use `uv run --no-sync` for commands. Linux/Docker Pillow wheels DO bundle
raqm, so production is unaffected.

## Deployment

`Dockerfile` (base `python:3.10-slim`, installs `libraqm-dev`) runs
`uv sync --frozen` and `uv run --no-sync python main.py`. In prod, set `IS_PROD`
to switch to webhook mode (`start_webhook`, `WEBHOOK_PATH`).

## Layout

- `zmanim_bot/main.py` — entry point (polling vs webhook).
- `zmanim_bot/config.py` — env-driven settings.
- `zmanim_bot/handlers/` — aiogram message/callback handlers (`main.py`,
  `festivals.py`, `settings.py`, `payments.py`, `geolocation.py`, …).
- `zmanim_bot/service/` — business logic that handlers call.
- `zmanim_bot/integrations/` — outbound HTTP clients (`zmanim_api_client.py`
  against `ZMANIM_API_URL`, geo/topo clients) and the pydantic response models
  in `zmanim_models.py`.
- `zmanim_bot/processors/image/renderer.py` — Pillow image rendering. **Pillow 10+
  notes:** use `font.getlength()` / `font.getbbox()`, not the removed `getsize()`;
  and never pass a font size of `0` to `ImageFont.truetype()` (now a `ValueError`) —
  `BaseImage.__init__` guards this since some subclasses set their real size only
  after `super().__init__()`.
- `zmanim_bot/repository/` — MongoDB access via odmantic (user storage).
- `zmanim_bot/middlewares/i18n.py` — babel-based i18n; `_()` / `lazy_gettext`.
- `zmanim_bot/texts/` — translatable strings (source for babel extraction).

## Conventions

- Keep all dependencies pinned; don't reintroduce unpinned deps (drift already
  caused one production outage — Pillow 10 removing `getsize`).
- `zmanim_bot/tasks.py` must stay free of app imports (no config/DB) so dev
  commands don't require `.env` or a database.
