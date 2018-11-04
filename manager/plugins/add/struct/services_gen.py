def app_template(plugin_name, user_name):
	return """from flask import Flask, jsonify
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
app.config['APPLICATION_ROOT'] = '/plugins/community/"""+user_name+"""/"""+plugin_name+"""'
#Ask user to sign-up first, before start using this plugin 


@app.route('/plugins/community/"""+user_name+"""/"""+plugin_name+"""/')
def """+plugin_name+"""():
    # raise
    return 'Hello World from community:"""+plugin_name+"""'

@login_required
@app.route('/plugins/community/"""+user_name+"""/"""+plugin_name+"""/info/')
def info():
    main = Main_algo()
    pid = os.getpid()
    url = 'http://localhost/api/sys/info/'
    return jsonify(main.currentProcessInfo(url+str(pid)))


@app.errorhandler(404)
def page_not_found(error):
    return f'<h1>"""+plugin_name+""" : 404<br>URL : {request.url}</h1>', 404"""


def wsgi_template():
    return """from werkzeug.debug import DebuggedApplication
from app import app as application

if application.debug:
        application.wsgi_app = DebuggedApplication(
            application.wsgi_app, evalex=True)

if __name__ == "__main__":
    application.run()
"""