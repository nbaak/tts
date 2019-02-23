FROM python:3.4.3

RUN pip install --upgrade pip && \
    pip install gTTS flask && \
    echo "DONE"

ADD src/ /tts/

EXPOSE 5000
ENTRYPOINT /tts/main.py
