FROM python:3.4.3

RUN pip install --upgrade pip && \
    pip install gTTS flask && \
    mkdir /tmp/mp3 && \
    echo "DONE"

ADD src/ /tts/

EXPOSE 5000
ENTRYPOINT /tts/main.py
