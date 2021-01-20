FROM python:3.7-slim-buster
COPY . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
ENV streamable_username ${streamable_username}
ENV streamable_password ${streamable_password}
ENV reddit_client_id ${reddit_client_id}
ENV reddit_client_secret ${reddit_client_secret}
ENV reddit_refresh_token ${reddit_refresh_token}
CMD python ./bot_streamable.py
