from flask import flash, Blueprint, render_template, render_template_string
from flask_plugins import connect_event


__plugin__ = "HelloWorld"

hello = Blueprint("hello", __name__, template_folder="templates")


def hello_world():
    flash("Hello World from {} Plugin".format(__plugin__), "success")


def hello_world2():
    flash("Hello World 2 from {} Plugin".format(__plugin__), "success")


def inject_hello_world():
    return "<h1>Hello World Injected</h1>"


def inject_hello_world2():
    return "<h1>Hello World 2 Injected</h1>"


def inject_navigation_link():
    return render_template_string(
        """
            <li><a href="{{ url_for('hello.index') }}">Hello</a></li>
        """
    )


@hello.route("/")
def index():
    return render_template("hello.html")


connect_event("tmpl_navigation_last", inject_navigation_link)
