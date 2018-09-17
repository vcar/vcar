import flask_plugins
from flask import (
    current_app, request, render_template, flash, redirect, url_for
)
from flask_login import login_required
from json2html import *

from . import dashboard
from ..constants.constants import PER_PAGE
from ..helpers.plugin import create_plugin, delete_plugin, ini2json
from ..models.plugin import Plugin
from ...extensions import db


# -------------------- /dashboard/plugin/ : List of plugins ------------------ #


@dashboard.route('/plugin/', methods=['GET'])
@login_required
def indexPlugin():
    plugins = Plugin.query.filter(Plugin.status != -1).paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )

    return render_template('dashboard/plugin/index.html', plugins=plugins)


# -------------------- /dashboard/plugin/id : Show plugin -------------------- #


@dashboard.route('/plugin/<int:id>', methods=['GET'])
@login_required
def showPlugin(id):
    plugin = Plugin.query.get_or_404(id)
    info = json2html.convert(json=plugin.info, table_attributes='class="table table-bordered table-striped"')
    init = json2html.convert(json=ini2json(plugin.init), table_attributes='class="table table-bordered table-striped"')

    return render_template('dashboard/plugin/show.html', plugin=plugin, info=info, init=init)


# -------------------- /dashboard/plugin/add  : Add new plugin ------------------ #


@dashboard.route('/plugin/add', methods=['GET', 'POST'])
@login_required
def addPlugin():
    blueprints = [str(x) for x in current_app.blueprints.keys()]
    state = '<div id="alertState"  style="display: none"></div>'
    visibility = '"block"'

    if request.method == 'POST':
        data = request.form
        state, visibility, return_val, created_plugin = create_plugin(data)

        if return_val['state']:
            plugin = Plugin(
                name=data['name'],
                identifier=created_plugin.plugin_name,
                logo=None,
                location=created_plugin.location,
                description=data['desc'],
                info=created_plugin.info_json,
                init=created_plugin.config_param,
                options="",
                version=created_plugin.plugin_version,
                status=1
            )

            db.session.add(plugin)
            db.session.commit()

            return redirect(url_for('dashboard.indexPlugin'))

    return render_template(
        "dashboard/plugin/add_plugin.html", form_display=visibility, state=state, blueprints_list=blueprints
    )


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


# -------------------- /dashboard/plugin/id/edit : Edit platform ----------------- #


@dashboard.route('/plugin/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editPlugin(id):
    """ Edit existing plugin """

    return render_template('dashboard/plugin/edit.html', id=id)


# ------------------ /dashboard/plugin/id/delete : Delete platform --------------- #


@dashboard.route('/plugin/<int:id>/delete', methods=['GET'])
@login_required
def deletePlugin(id):
    plugin = Plugin.query.get_or_404(id)
    plugin.status = -1
    new_location = delete_plugin(plugin)

    if new_location is not False:
        plugin.location = new_location
        db.session.commit()
        flash('Plugin {}, deleted successfully.'.format(plugin.name), 'success')
    else:
        flash('Plugin {}, could not be deleted.'.format(plugin.name), 'error')

    return redirect(url_for('dashboard.indexPlugin'))
