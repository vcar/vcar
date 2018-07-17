from flask import Flask
from flask import request

app = Flask(__name__)
app.debug = True
app.config["APPLICATION_ROOT"] = "/plugins/community/root/p1"

@app.route('/')
def index():
    # raise
    return "Holaaa"

@app.route('/plugins/community/root/p1/')
def p1():
    # raise
    return "Hello World from community:p11"

@app.errorhandler(404)
def page_not_found(error):
    return f"<h1>P1 : 404<br>URL : {request.url}</h1>", 404
