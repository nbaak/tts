FROM python:latest

RUN pip3 install --upgrade pip && \
    pip3 install gTTS flask && \
    echo "DONE"

ADD src/ /tts/

EXPOSE 5000
ENTRYPOINT /tts/main.py
