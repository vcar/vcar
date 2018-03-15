from flask import (
    render_template, flash, redirect, url_for
)
import flask_plugins
from flask_login import login_required

from . import dashboard

# -------------------- /dashboard/plugin/ : List of plugins ------------------ #


@dashboard.route('/plugin/', methods=['GET'])
@login_required
def indexPlugin():
    plugins = flask_plugins.get_all_plugins()
    try:
        plugins = flask_plugins.get_all_plugins()
    except Exception:
        plugins = None

    # raise

    return render_template('dashboard/plugin/index.html', plugins=plugins)

# -------------------- /dashboard/plugin/id : Show plugin -------------------- #


@dashboard.route('/plugin/<identifier>', methods=['GET'])
@login_required
def showPlugin(identifier):
    try:
        plugin = flask_plugins.get_plugin_from_all(identifier)
    except Exception:
        plugin = None

    return render_template('dashboard/plugin/show.html', plugin=plugin)

# -------------------- /dashboard/plugin/id/enable : Enable plugin ----------- #


@dashboard.route('/plugin/<identifier>/enable', methods=['GET'])
@login_required
def enablePlugin(identifier):
    try:
        enabled = flask_plugins.get_plugin_from_all(identifier)
        flash('Plugin {}, updated successfully.'.format(identifier), 'success')
    except Exception:
        enabled = None

    if enabled:
        flash('Plugin {}, enabled successfully.'.format(identifier), 'success')
    else:
        flash('Plugin {}, not enabled.'.format(identifier), 'error')

    return redirect(url_for('dashboard.indexPlugin'))
