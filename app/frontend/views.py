from flask import Blueprint, request, render_template

frontend = Blueprint('frontend', __name__, url_prefix='/')

# ------------------------------- /api/ : Api ------------------------------- #


@frontend.route('/')
def index():
    home = {
        'title': "xx",
        'sub_title': "sub title",
        'Other': " bla bla bla ..."
    }
    return render_template('frontend/index.html')


# ---------------------------- /kill : kill Server ------------------------- #


@frontend.route('about')
def about():
    return "About : vCar Platform !"


# ---------------------------- /kill : kill Server ------------------------- #


@frontend.route('kill')
def killo():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "Flask Development Server killed successfully!"
