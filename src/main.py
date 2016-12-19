#!/usr/bin/env python3

from flask import Flask, abort, redirect, url_for, Response, jsonify, send_file
from gtts import gTTS
from lib.Config import Config

import uuid, hashlib, os, urllib

app = Flask(__name__)
cfg = Config(os.path.dirname(__file__)+'/config.json')

history = []

def add_to_history(lang, text):
    content_hash = str(hashlib.md5(lang.encode()+text.encode()).hexdigest())
    link = '<div class="link"><a href='+cfg.server_host+":"+str(cfg.public_port)+"/tts/"+lang+"/"+urllib.parse.quote(text)+">"+text+"</a></div>"
    if link not in history:
        history.append(link)
    

def tts (lang, text):
    id = str(uuid.uuid4())
    content_hash = str(hashlib.md5(lang.encode()+text.encode()).hexdigest())
    text = text.replace('+', ' ')
    print ("\nLang: %s\nText: %s" % (lang, text))
    print ("hash %s" % content_hash)
    tts = gTTS(text, lang=lang)
    file_name = '/tmp/mp3/'+content_hash+'.mp3'
    print ("File: %s" % file_name)
    tts.save(file_name)
    add_to_history(lang, text)
    return send_file(file_name)

@app.route("/tts/<text>", methods=["GET"])
def get_tts_slim(text):
    return tts(cfg.default_language, text)

@app.route("/tts/<lang>/<text>", methods=['GET'])
def get_tts(lang, text):
    return tts(lang, text)

@app.route("/history", methods=["GET"])
def get_history():
    if cfg.history_enabled != 'enabled':
        abort(404)
    payload = '<div class="links">'
    for link in history:
        payload += link
    payload += "</div>"
    print (history)
    print (payload)
    return payload

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int(cfg.port))