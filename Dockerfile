FROM python:3.10-slim

RUN apt update && apt install -y libraqm-dev

# uv package manager (pinned)
COPY --from=ghcr.io/astral-sh/uv:0.7.3 /uv /uvx /bin/

WORKDIR /home/app
COPY . .

# Install locked dependencies into /home/app/.venv
# (uv fetches the managed CPython 3.10.7 required by pyproject.toml)
RUN uv sync --frozen

ENV PYTHONPATH=/home/app
ENV DOCKER_MODE=true
EXPOSE 8000

WORKDIR /home/app/zmanim_bot
CMD ["uv", "run", "--no-sync", "python", "main.py"]
