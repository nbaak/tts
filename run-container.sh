#!/bin/bash

docker rm -f tts
docker run -p 5000:5000 \
    --name=tts \
    -d k3nny/tts