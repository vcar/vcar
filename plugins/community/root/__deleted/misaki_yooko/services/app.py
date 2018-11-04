from flask import Flask
from flask import request

app = Flask(__name__)
app.debug = True
app.config['APPLICATION_ROOT'] = '/plugins/community/root/misaki_yooko'

@app.route('/')
def index():
    # raise
    return 'Holaaa'

@app.route('/plugins/community/root/misaki_yooko/')
def misaki_yooko():
    # raise
    return 'Hello World from community:misaki_yooko'

@app.errorhandler(404)
def page_not_found(error):
    return f'<h1>misaki_yooko : 404<br>URL : {request.url}</h1>', 404