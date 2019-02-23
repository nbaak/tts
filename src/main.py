#!/usr/bin/env python3

from flask import Flask, abort, redirect, url_for, Response, jsonify, send_file
from gtts import gTTS
from lib.Config import Config
from lib.KeyValueStore import KeyValueStore as KVS

import uuid, hashlib, os, urllib

app = Flask(__name__)
cfg = Config(os.path.dirname(__file__)+'/config.json')
history = KVS()
FILE_ROOT = os.path.dirname(__file__)+'/mp3_files/'

def initialize():
    if not os.path.isdir(FILE_ROOT):
        print ("created dir: {}".format(FILE_ROOT))
        os.makedirs(FILE_ROOT)      
        

def add_to_history(hash, file_name, lang, text):
    history.add_key(hash, file_name)
    history.add_attribute(hash, "lang", lang)
    history.add_attribute(hash, "text", text)
    
    link = '<div class="link"><a href='+cfg.server_host+":"+str(cfg.public_port)+"/tts/"+lang+"/"+urllib.parse.quote(text)+">"+lang+" - " +text+"</a></div>"   

def tts (lang, text): 
    text = text.replace('+', ' ')   
    tts = gTTS(text, lang=lang)
    
    content_hash = str(hashlib.md5(lang.encode()+text.encode()).hexdigest())
    file_name = FILE_ROOT+content_hash+'.mp3'
    
    tts.save(file_name)
    add_to_history(content_hash, file_name, lang, text)
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
    for item in history.store:
        lang = history.get_attribute(item, 'lang')
        text = history.get_attribute(item, 'text')        
        payload += '<div class="link">'
        payload += '<a href="'+cfg.server_host+':'+str(cfg.public_port)+'/tts/'+lang+'/'+text+'">'+lang+' - '+text
        payload += '</a></div>'
    payload += "</div>"
    return payload

if __name__ == '__main__':
    initialize()
    app.run(host='0.0.0.0', debug=False, port=int(cfg.port))