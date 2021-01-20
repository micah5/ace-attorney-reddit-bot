FROM python:3.7-slim-buster
COPY . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
CMD python ./bot_streamable.py
