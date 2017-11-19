from flask import Blueprint, render_template
from app.plugins.helpers import render_md

from .algorithms.drivergraph import DriverGraph
from .algorithms.settings import DefaultSettings

from .. import __path__

driverGraph = Blueprint(
    "driverGraph",
    __name__,
    url_prefix='/driver_graph',
    template_folder="../templates"
)

# --------------------- /driver_graph/ : Overview --------------------------- #


@driverGraph.route("/")
def index():

    html = render_md(__path__, "README.md")

    return render_template("index.html", html=html)

# --------------------- /driver_graph/datasets : Show available datasets ---- #


@driverGraph.route("/datasets")
def datasets():
    # todo
    return render_template("datasets.html")

# --------------------- /driver_graph/run : Main plugin function ------------ #


@driverGraph.route("/run")
def run():
    driver = DriverGraph(max_nodes=30)
    driver.settings = DefaultSettings
    driver.create_digraph("/home/karim/OpenXC/uptown-west.json")
    graph_js = driver.vis_network(physics=True)

    return render_template("run.html", graph_js=graph_js)

# --------------------- /driver_graph/custom : custom functions ------------- #


@driverGraph.route("/custom")
def custom():
    # some plugin spesific functions ...

    return render_template("custom.html")

# --------------------- /driver_graph/docs : Documentation ------------------ #


@driverGraph.route("/docs")
def docs():
    # documentation in markdown
    html = render_md(__path__, "DOC.md")

    return render_template("docs.html", html=html)
