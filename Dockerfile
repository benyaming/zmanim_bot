FROM python:3.9-slim

RUN pip install pipenv
WORKDIR /home/app
COPY . .
WORKDIR /home/app/zmanim_bot
RUN pipenv update
ENV PYTHONPATH=/home/app
ENV DOCKER_MODE=true
EXPOSE 8000
CMD ["pipenv", "run", "python", "main.py"]
