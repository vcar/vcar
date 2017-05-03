from flask import Blueprint, render_template, current_app

import flask_plugins

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
    # x = current_app
    # y = flask_plugins.get_enabled_plugins()
    # raise
    driver = DriverGraph(settings=DefaultSettings, max_nodes=35)
    driver.create_digraph("/home/karim/OpenXC/downtown-crosstown.json")
    html = driver.vis_network(physics=True)

    return render_template("graph.html", html=html)

@driverGraph.route("/l")
def light():
    driver = DriverGraph(settings=DefaultSettings, max_nodes=50)
    driver.create_digraph("/home/karim/OpenXC/downtown-crosstown.json")
    html = driver.vis_network(physics=True)

    return render_template("graph._light.html", html=html)
