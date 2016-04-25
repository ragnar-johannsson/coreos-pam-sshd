#!/usr/bin/env python

from Crypto.PublicKey import RSA
from flask import Flask, abort, request
from os import environ

app = Flask(__name__)
keys = {}
state_secret = environ.get('SECRET', '')

@app.route('/generate/<username>/<secret>', methods=['GET'])
def generate(username, secret):
    if secret != state_secret:
        abort(401)
    keypair = RSA.generate(2048)
    keys[username] = keypair.publickey().exportKey('OpenSSH')
    return keypair.exportKey('PEM'), 200

@app.route('/retrieve/<username>', methods=['GET'])
def retrieve(username):
    try:
        return keys.pop(username), 200
    except:
        return '', 200

app.run(host='0.0.0.0', port=1730)
