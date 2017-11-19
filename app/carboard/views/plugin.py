from flask import (
    render_template, flash, redirect, url_for
)
import flask_plugins
from flask_login import login_required

from . import carboard

# -------------------- /carboard/plugin/ : List of plugins ------------------ #


@carboard.route('/plugin/', methods=['GET'])
@login_required
def indexPlugin():
    plugins = flask_plugins.get_all_plugins()
    try:
        plugins = flask_plugins.get_all_plugins()
    except Exception:
        plugins = None

    # raise

    return render_template('carboard/plugin/index.html', plugins=plugins)

# -------------------- /carboard/plugin/id : Show plugin -------------------- #


@carboard.route('/plugin/<identifier>', methods=['GET'])
@login_required
def showPlugin(identifier):
    try:
        plugin = flask_plugins.get_plugin_from_all(identifier)
    except Exception:
        plugin = None

    return render_template('carboard/plugin/show.html', plugin=plugin)

# -------------------- /carboard/plugin/id/enable : Enable plugin ----------- #


@carboard.route('/plugin/<identifier>/enable', methods=['GET'])
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

    return redirect(url_for('carboard.indexPlugin'))
