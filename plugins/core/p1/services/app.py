from flask import Flask
from flask import request

app = Flask(__name__)
app.debug = True

@app.route('/plugins/core/p1/')
def index():
    # raise
    return "Hello World from p1"

@app.errorhandler(404)
def page_not_found(error):
    # return f"<h1>P1 : 404<br>URL : {request.url}</h1>", 404
    return "<h1>P1 : 404<br>URL : {url}</h1>".format(url=request.url), 404

