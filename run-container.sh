#!/bin/bash

docker rm -f tts_webservice
docker run -p 5000:5000 \
    --name=tts_webservice \
    -d k3nny/tts