FROM python:3.10-slim

RUN apt update
RUN apt install -y libraqm-dev

RUN pip install pdm
WORKDIR /home/app
COPY . .
WORKDIR /home/app/zmanim_bot
RUN pipenv install
ENV PYTHONPATH=/home/app
ENV DOCKER_MODE=true
EXPOSE 8000
CMD ["pdm", "run", "python", "main.py"]
