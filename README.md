# PYTHON TTS WITH FLASK
... Using gTTS API

## Config (./src/config.py)
set your host and enabled or disable the history


## deployment
`docker-compose build` building the image

`docker-compuse up -d` start the contaier

`docker-compose down -v` if you want to shut down the service


## usage
Inside the container runs a python3 Flask Server which understands the command
/tts/<text>
or
/tts/<lang>/<text>
The server will return with an mp3 file of the text