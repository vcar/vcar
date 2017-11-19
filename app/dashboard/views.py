import os
from os.path import basename
import json
from werkzeug import secure_filename
from threading import Thread, active_count
from flask import (
    Blueprint, render_template, request, flash, redirect, url_for, Response
)
from flask_login import (
    login_user, logout_user, login_required, current_user
)

from .models import Trace
from .drivergraph import DriverGraph
from .helpers import upload_trace, debug
from .tasks import task_info, openxc_task
from ..extensions import db

from elasticsearch import Elasticsearch, helpers


dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


# -------------------- /dashboard : Dashboard home page -------------------- #

# @dashboard.route('/stream')
# def stream():
#     return Response(task_info(), mimetype="text/event-stream")


@dashboard.route('/')
@login_required
def index():
    return render_template('dashboard/index.html', user=current_user)

# ------------------------- /import : Import Addons ------------------------- #


@dashboard.route('/import')
@login_required
def import_index():
    return render_template('dashboard/import/index.html', user=current_user)

# __________________________________________________________________________ #
# |                                                                        | #
# |                                  OPENXC                                | #
# |                                                                        | #
# __________________________________________________________________________ #

# ---------------- /dashboard/import/openxc : User home page --------------- #


@dashboard.route('/import/openxc', methods=['GET', 'POST'])
@login_required
def import_openxc():
    if request.method == 'POST':
        openxc = upload_trace('openxc', current_user.id)
        if openxc['status'] is True:
            trace = Trace(
                user_id=current_user.id,
                filename=basename(openxc['message']),
                path=openxc['message']
            )
            db.session.add(trace)
            db.session.commit()
        return json.dumps(openxc)
    return render_template('dashboard/import/openxc.html', user=current_user)

# --------------- /import/openxc/process : Process openxc file ------------- #


@dashboard.route('/import/openxc/process', methods=['GET', 'POST'])
@login_required
def process_openxc():
    if request.method == 'POST':
        traces = request.form.getlist('traces')
        thread = Thread(target=openxc_task, args=[traces, current_user.id])
        thread.daemon = True
        thread.start()
        # thread.join(1)
        # print(active_count())
    else:
        return redirect(url_for('dashboard.import_openxc'))
    return render_template(
        'dashboard/import/openxc_porcess.html',
        user=current_user
    )

# ------------------------- /openxc : Openxc Dashboard ---------------------- #


@dashboard.route('/openxc/', methods=['GET'])
@login_required
def openxc():
    info = {
        index: 'openxc',
        type: 'driver_{}'.format(current_user.id)
    }
    return render_template(
        'dashboard/openxc.html',
        user=current_user,
        elastic=info
    )

# -------------------------- /openxc/map : Openxc Map ----------------------- #


@dashboard.route('/openxc/map', methods=['GET'])
@login_required
def openxc_map():
    info = {
        index: 'openxc',
        type: 'driver_{}'.format(current_user.id)
    }
    return render_template(
        'dashboard/openxc_map.html',
        user=current_user,
        elastic=info
    )

# ------------------------ /openxc/graph : Openxc Graph --------------------- #


@dashboard.route('/openxc/graph', methods=['GET'])
@login_required
def openxc_graph():
    index = "openxc"
    type = "driver_{}".format(current_user.id)
    size = 10000
    es = Elasticsearch([{
        'host': 'localhost',
        'port': 9200
    }])
    es.cluster.health(wait_for_status='yellow', request_timeout=1)
    if es.indices.exists(index=index):
        body = {
            "sort": [
                {"timestamp": {"order": "asc"}}
            ],
            "query": {
                "bool": {
                    "should": [
                        {"term": {"name": 'vehicle_speed'}},
                        {"term": {"name": 'engine_speed'}},
                        {"term": {"name": 'fuel_level'}},
                        {"term": {"name": 'torque_at_transmission'}},
                        {"term": {"name": 'transmission_gear_position'}}
                    ]
                }
            }
        }
        res = es.search(index=index, doc_type=type, size=size, body=body)
        # print("Got {} Hits:".format(res['hits']['total']))
        # for hit in res['hits']['hits']:
        # print("%(timestamp)s %(name)s: %(value)s" % hit["_source"])
        if res['hits']['total'] > 0:
            driver = DriverGraph()
            driver.build_digraph(res)
            graph = driver.vis_network(True)

    info = {
        index: 'openxc',
        type: 'driver_{}'.format(current_user.id)
    }
    return render_template(
        'dashboard/openxc_graph.html',
        user=current_user,
        elastic=info,
        graph=graph
    )

# ---------------------------- /kill : kill Server ------------------------- #


# @dashboard.route('/kill')
# def killo():
#     func = request.environ.get('werkzeug.server.shutdown')
#     if func is None:
#         raise RuntimeError('Not running with the Werkzeug Server')
#     func()
#     return "Flask Development Server killed successfully!"


@dashboard.route('/restart')
def restart_server():
    os.kill(os.getpid(), signal.SIGHUP)
