from flask import Blueprint, render_template

api = Blueprint('api', __name__, url_prefix='/api')

# ------------------------------- /api/ : Api ------------------------------- #


@api.route('/')
def index():
    x = "API Blueprint"
    return render_template('index.html', user=x)
