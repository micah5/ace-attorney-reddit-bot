FROM python:3.7-slim-buster
WORKDIR /app

COPY requirements.txt .
RUN apt-get update && \
  apt-get install ffmpeg libsm6 libxext6 -y && \
  pip install -r requirements.txt && \
  python -m spacy download en_core_web_sm && \
  apt-get clean && \
  rm -rf ~/.cache/pip/*

COPY . .

ENV streamable_username ${streamable_username}
ENV streamable_password ${streamable_password}
ENV reddit_client_id ${reddit_client_id}
ENV reddit_client_secret ${reddit_client_secret}
ENV reddit_refresh_token ${reddit_refresh_token}

CMD python ./bot_streamable.py
