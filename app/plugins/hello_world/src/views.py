from flask import Blueprint, render_template, current_app

import flask_plugins

hello = Blueprint(
    "hello",
    __name__,
    url_prefix='/hello',
    template_folder="../templates"
)

"""
TODO :
    - Check app context
        with app.app_context():
            cur = db.connection.cursor()
            cur.execute(...)
"""


@hello.route("/")
def index():
    # a = current_app
    # b = flask_plugins.get_enabled_plugins()
    # c = flask_plugins.get_all_plugins()
    # d = flask_plugins.get_plugin_from_all('driver_graph')
    # try:
    #     x = flask_plugins.get_plugin('driver_graph')
    # except KeyError, e:
    #     x = None

    # x = flask_plugins.get_plugin_from_all('hello_world')
    # y = flask_plugins.get_plugin_from_all('driver_graph')
    # raise

    # 'Yeaah' if y.enabled is True else 'Noooo' ==> 'Noooo'
    # y.path ==>'/home/karim/OpenXC/Dashboard/Flask/vcar/app/plugins/driver_graph'
    # y.name ==> 'Driver Graph'
    # y.identifier ==> 'driver_graph'
    # y.description ==> 'Generate driver behavoir graph.'
    # y.description_lc ==> {'en': u'Generate driver behavoir graph.'}
    # y.author ==> 'boubouhkarim'
    # y.license ==> 'BSD'
    # y.version ==> '1.0.0'

    # y.enable() ==> enable the plugin by removing DESABLED
    #

    return render_template("hello.html")
