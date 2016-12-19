#!/bin/bash

docker rmi -f k3nny/tts
docker build -t k3nny/tts .
