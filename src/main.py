#!/usr/bin/env python3

from flask import Flask, abort, send_file
from gtts import gTTS
from lib.KeyValueStore import KeyValueStore as KVS

import config as cfg
import hashlib, os

app = Flask(__name__)

history = KVS()
FILE_ROOT = os.path.join(os.path.dirname(__file__), 'mp3_files/')


def initialize():
    if not os.path.isdir(FILE_ROOT):
        print (f"created dir: {FILE_ROOT}")
        os.makedirs(FILE_ROOT)


def add_to_history(text_hash, file_name, lang, text):
    history.add_key(text_hash, file_name)
    history.add_attribute(text_hash, "lang", lang)
    history.add_attribute(text_hash, "text", text)


def tts(file_format, lang, text):
    if cfg.max_string_size > 0 and len(text) > cfg.max_string_size:
        return "text_too_long"

    text = text.replace('+', ' ')
    tts = gTTS(text, lang=lang)

    content_hash = str(hashlib.md5(lang.encode() + text.encode()).hexdigest())
    file_name = f"{FILE_ROOT}{content_hash}.{file_format}"

    if not os.path.exists(file_name):
        tts.save(file_name)

    if cfg.history_enabled:
        add_to_history(content_hash, file_name, lang, text)

    return send_file(file_name)


@app.route("/tts/<text>", methods=["GET"])
def get_tts_slim(text):
    return tts(cfg.default_format, cfg.default_language, text)


@app.route("/tts/<lang>/<text>", methods=['GET'])
def get_tts(lang, text):
    return tts(cfg.default_format, lang, text)


@app.route("/tts/<format>/<lang>/<text>", methods=['GET'])
def get_tts_format(format, lang, text):
    return tts(format, lang, text)


@app.route("/history", methods=["GET"])
def get_history():
    if not cfg.history_enabled:
        abort(404)

    payload = '<div class="links">'
    for item in history.store:
        lang = history.get_attribute(item, 'lang')
        text = history.get_attribute(item, 'text')
        payload += '<div class="link">'
        payload += '<a href="' + cfg.server_host + ':' + str(cfg.public_port) + '/tts/' + lang + '/' + text + '">' + lang + ' - ' + text
        payload += '</a></div>'
    payload += "</div>"
    return payload


if __name__ == '__main__':
    initialize()
    app.run(host='0.0.0.0', debug=cfg.debug_mode, port=int(cfg.port))

