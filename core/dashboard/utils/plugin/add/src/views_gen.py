def views_template(plugin_name):
	return """
from flask import Blueprint, Response, request, render_template, jsonify, current_app
import flask_plugins
from flask_login import (
    login_user, logout_user, login_required, current_user
)
from core.dashboard.helpers.markdown import render_md
from .. import __path__

"""+plugin_name+""" = Blueprint('"""+plugin_name+"""', __name__, url_prefix='/"""+plugin_name+"""', template_folder="../View/templates", static_folder="../View/static")
from .algorithms.main import Main_algo


@"""+plugin_name+""".route("/")
def index():
    main = Main_algo()
    somebody_name = "there"
    message = main.salutation(somebody_name)["msg"]

    return render_template('"""+plugin_name+"""/index.html', html="<h1>"+message+"</h1>")


@"""+plugin_name+""".route("/docs")
def docs():
    # documentation in markdown
    html = render_md(__path__, "Docs/DOC.md")
    return render_template('"""+plugin_name+"""/docs.html', html=html)

"""