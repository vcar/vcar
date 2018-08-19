def app_template(plugin_name, user_name):
	return """from flask import Flask
from flask import request

app = Flask(__name__)
app.debug = True
app.config['APPLICATION_ROOT'] = '/plugins/community/"""+user_name+"""/"""+plugin_name+"""'

@app.route('/')
def index():
    # raise
    return 'Holaaa'

@app.route('/plugins/community/"""+user_name+"""/"""+plugin_name+"""/')
def """+plugin_name+"""():
    # raise
    return 'Hello World from community:"""+plugin_name+"""'

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