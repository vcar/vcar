from flask import Blueprint, render_template

from .algorithms.drivergraph import DriverGraph
from .algorithms.settings import DefaultSettings

driverGraph = Blueprint(
    "driverGraph",
    __name__,
    url_prefix='/driver_graph',
    template_folder="../templates"
)

"""
TODO :
    - Check app context
        with app.app_context():
            cur = db.connection.cursor()
            cur.execute(...)

    - Done :)
"""


@driverGraph.route("/")
def index():
    driver = DriverGraph(max_nodes=30)
    driver.settings = DefaultSettings
    driver.create_digraph("/home/karim/OpenXC/uptown-west.json")
    graph_js = driver.vis_network(physics=True)

    return render_template("graph.html", graph_js=graph_js)


@driverGraph.route("/docs")
def docs():

    return render_template("graph.html")
