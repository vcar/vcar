from flask import Flask, jsonify
from flask import request
from flask_login import login_required
import psutil
import os, inspect

###
import sys
sys.path.append('../workspace/')
from algorithms.main import Main_algo
###

app = Flask(__name__)
app.debug = True
app.config['APPLICATION_ROOT'] = '/plugins/community/root/gPI'
#Ask user to sign-up first, before start using this plugin 


@app.route('/plugins/community/root/gPI/')
def gPI():
    # raise
    return 'Hello World from community:gPI'

@login_required
@app.route('/plugins/community/root/gPI/info/')
def info():
    main = Main_algo()
    pid = os.getpid()
    url = 'http://localhost/api/sys/info/'
    return jsonify(main.currentProcessInfo(url+str(pid)))


@app.errorhandler(404)
def page_not_found(error):
    return f'<h1>gPI : 404<br>URL : {request.url}</h1>', 404