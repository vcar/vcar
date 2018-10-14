from flask import Blueprint
from flask_login import login_required

from .blog.endpoints.add_plugin import ns as add_plugin_namespace
from .blog.endpoints.current_system_status import ns as sys_info_namespace

from .restplus import rest_api
import os
import signal

"""
    This package should represent the vCar API main package

"""

api = Blueprint('api', __name__, url_prefix='/api')
rest_api.init_app(api)
rest_api.add_namespace(add_plugin_namespace)
rest_api.add_namespace(sys_info_namespace)


@login_required
@api.route('/restart-server')
def restart_server():
    # To do ...
    """
        To restart the application by sending a HUP signal to the application server.
        The following code snippets, are showing how this can be done with the WSGI server gunicorn.
        Gunicorn has be to started in daemon (--daemon) mode in order for this to work.
    """
    os.kill(os.getpid(), signal.SIGHUP)