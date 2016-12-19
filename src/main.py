#!/usr/bin/env python3

from flask import Flask, abort, redirect, url_for, Response, jsonify, send_file
from gtts import gTTS
from lib.Config import Config

import uuid, hashlib, os

app = Flask(__name__)
cfg = Config(os.path.dirname(__file__)+'/config.json')

def tts (lang, text):
    if len(text) > cfg.max_string_size:
        return "String Size Error!"
    id = str(uuid.uuid4())
    content_hash = str(hashlib.md5(lang.encode()+text.encode()).hexdigest())
    text = text.replace('+', ' ')
    print ("\nLang: %s\nText: %s" % (lang, text))
    print ("hash %s" % content_hash)
    tts = gTTS(text, lang=lang)
    file_name = '/tmp/mp3/'+content_hash+'.mp3'
    print ("File: %s" % file_name)
    tts.save(file_name)
    return send_file(file_name)

@app.route("/tts/<text>", methods=["GET"])
def get_tts_slim(text):
    return tts(cfg.default_language, text)

@app.route("/tts/<lang>/<text>", methods=['GET'])
def get_tts(lang, text):
    return tts(lang, text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=cfg.port)