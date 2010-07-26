#!/usr/bin/env python
## app.py -- Demo app -*- Python -*-
## Time-stamp: "2010-07-26 20:02:30 ghoseb"
## Author: Baishampayan Ghose <bg@infinitelybeta.com>

## Copyright (c) 2010, InfinitelyBeta.com

import os
from base64 import b64encode

from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

__path = os.getcwd() + "/static/img/"
__ext = ".gif"

def encode_img(img_id):
    file_name = "%s%s%s" % (__path, img_id, __ext)
    try:
        fd = open(file_name, 'rb')
        b64data = b64encode(fd.read())
        fd.close()
        return img_id, b64data
    except IOError:
        return img_id, None     # no such file


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/more/')
def more():
    return render_template('more.html')


@app.route('/stylesheets/logos.css')
def datauri():
    req_arg = request.args.get('i', None)
    if req_arg:
        img_ids = req_arg.split('|')
        cxt = [{"img" : c, "data" : d} for c, d in (encode_img(i) for i in img_ids) if d != None]
        resp = app.make_response(render_template('logos.css', data=cxt))
        resp.headers['Content-Type'] = 'text/css'
        return resp
    return ''

if __name__ == '__main__':
    app.run(debug=True)

