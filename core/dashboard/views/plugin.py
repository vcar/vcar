import json
from multiprocessing.pool import ThreadPool
from flask import (
    current_app, request, render_template, flash, redirect, url_for
)
import flask_plugins
from flask_login import login_required

from . import dashboard
from ..utils.plugin.add import CreateNewPlugin


# -------------------- /dashboard/plugin/add  : Add new plugin ------------------ #


@dashboard.route('/plugin/add', methods=['GET', 'POST'])
@login_required
def addPlugin():

    used_blueprints = [str(x) for x in current_app.blueprints.keys()]
    html_alertState = '<div id="alertState"  style="display: none"></div>'
    visibility = '"block"'
    if request.method == 'POST':
        plugin_name = request.form['name']
        desc = request.form['desc']
        author_name = request.form['author_name']
        author_mail = request.form['author_mail']
        contributors_names = (
            str(request.form['contributors_names']).replace(", ", ",")).split(',')
        license_type = request.form['license_type']
        plugin_version = request.form['plugin_version']
        python_version = request.form['pythonVersion']
        plugin_requirements = request.form['pluging_requirements']
        some_additional_interface = json.loads(
            str(request.form['interface_results']).replace("\r\n", ""))
        print("========================\n\n\nAPI Interface:\n========================\n{}\n========================\n\n\n".format(
            some_additional_interface))

        #raise

        try:
            thread_function = CreateNewPlugin(plugin_name, desc, author_name, author_mail, python_version,
                                              plugin_requirements, contributors_names, some_additional_interface, license_type, plugin_version)
            pool = ThreadPool(processes=1)
            async_result = pool.apply_async(thread_function.run, ())
            return_val = async_result.get()

            if return_val == "True":
                '''Plugin has been created successfully'''
                flash(
                    plugin_name+' plugin has been created successfully ('+str(return_val)+') !')
                alert_type = "alert-success"
                msg_head = "Well done!"
                msg_content = "Your plugin has been created successfully"
                msg_info = "Whenever you need to, be sure to restart the server before you start using this Plugin."
                button_html = '<a class="btn btn-primary" href="/dashboard/plugin/add" role="button">Create a New Plugin</a>'

            elif return_val == "False":
                '''Plugin name already exist'''
                flash(plugin_name+' plugin name already exist ('+str(return_val)+') !')
                alert_type = "alert-warning"
                msg_head = "WARNING : the plugin name already exist!"
                msg_content = "Please try another name"
                msg_info = "Expamle : my name ==> my name_nbr or my name nbr ..."
                button_html = '<button class="btn btn-primary" onclick="display_none()">' +\
                              '<span class="glyphicon glyphicon-arrow-left" aria-hidden="true"></span>Try Again' +\
                              '</button>'

            else:
                '''ERROR !'''
                pass
                raise

        except Exception as e:
            flash('ERROR! Plugin has not been created! : {}'.format(str(e)))

            alert_type = "alert-danger"
            msg_head = "Oops! Something went wrong!"
            msg_content = "Try again with a different Plugin name"
            msg_info = "If you get this message again, please do not hesitate to contact us"
            button_html = '<button class="btn btn-primary" onclick="display_none()">' +\
                          '<span class="glyphicon glyphicon-arrow-left" aria-hidden="true"></span>Try Again' +\
                          '</button>'

        html_alertState = '<div id="alertState" class="col-md-11"><div class="form-group alert '+alert_type+'" role="alert">' +\
            '<h4 class="alert-heading">'+msg_head+'</h4>' +\
            '<p>'+msg_content+'</p>' +\
            '<hr>' +\
            '<p class="mb-0">'+msg_info+'</p>' +\
            '</div>' +\
            '<div class="form-group">'+button_html+'</div></div>'
        visibility = '"none"'

    return render_template("dashboard/plugin/add_plugin.html", form_display=visibility, state=html_alertState, blueprints_list=used_blueprints)


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
