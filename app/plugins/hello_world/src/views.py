from flask import Blueprint, render_template
from app.plugins.helpers import render_md

from .. import __path__

hello = Blueprint(
    "hello",
    __name__,
    url_prefix='/hello',
    template_folder="../templates"
)

# --------------------- /hello/ : Overview --------------------------- #


@hello.route("/")
def index():

    # Hello world is a one page plugin

    html = render_md(__path__, "README.md")

    return render_template("hello_world/index.html", html=html)
