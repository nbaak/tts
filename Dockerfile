FROM python:latest

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install ffmpeg -y && \
    pip3 install --upgrade pip && \
    pip3 install gTTS flask pydub && \
    echo "DONE"

ADD src/ /tts/

EXPOSE 5000
ENTRYPOINT /tts/main.py
