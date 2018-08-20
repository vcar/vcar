from flask import Flask
from flask import request

app = Flask(__name__)
app.debug = True
app.config['APPLICATION_ROOT'] = '/plugins/community/root/new_gen_plugin'

@app.route('/')
def index():
    # raise
    return 'Holaaa'

@app.route('/plugins/community/root/new_gen_plugin/')
def new_gen_plugin():
    # raise
    return 'Hello World from community:new_gen_plugin'

@app.errorhandler(404)
def page_not_found(error):
    return f'<h1>new_gen_plugin : 404<br>URL : {request.url}</h1>', 404