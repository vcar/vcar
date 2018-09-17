import configparser
import json
import os
from multiprocessing.pool import ThreadPool

from flask import flash

from manager.plugins.add import CreateNewPlugin


def create_plugin(data):
    return_val = None
    thread_function = None

    plugin_name = data['name']
    desc = data['desc']
    author_name = data['author_name']
    author_mail = data['author_mail']
    contributors_names = (
        str(data['contributors_names']).replace(", ", ",")).split(',')
    license_type = data['license_type']
    plugin_version = data['plugin_version']
    python_version = data['pythonVersion']
    plugin_requirements = data['pluging_requirements']
    some_additional_interface = json.loads(
        str(data['interface_results']).replace("\r\n", ""))

    thread_function = CreateNewPlugin(
        plugin_name, desc, author_name, author_mail, python_version, plugin_requirements,
        contributors_names, some_additional_interface, license_type, plugin_version
    )

    try:
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(thread_function.run, ())
        return_val = async_result.get()

        alert_type = "alert-success"
        msg_head = "Well done!"
        msg_content = "Your plugin has been created successfully"
        msg_info = "Whenever you need to, be sure to restart the server before you start using this Plugin."
        button_html = '<a class="btn btn-primary" href="/dashboard/plugin/add" role="button">Create a New Plugin</a>'

        if return_val["state"] == True:
            '''Plugin has been created successfully'''
            flash(f"<b>{plugin_name}</b> : {return_val['message']}")
        elif return_val:
            '''Plugin name already exist'''
            flash(return_val["message"])
            alert_type = "alert-warning"
            msg_head = "WARNING : the plugin name already exist!"
            msg_content = "Please try another name"
            msg_info = "Expamle : my name ==> my name_nbr or my name nbr ..."
            button_html = '<button class="btn btn-primary" onclick="display_none()">' + \
                          '<span class="glyphicon glyphicon-arrow-left" aria-hidden="true"></span>Try Again' + \
                          '</button>'

    except Exception as e:
        flash('ERROR! Plugin has not been created! : {}'.format(str(e)))

        alert_type = "alert-danger"
        msg_head = "Oops! Something went wrong!"
        msg_content = "Try again with a different Plugin name"
        msg_info = "If you get this message again, please do not hesitate to contact us"
        button_html = '<button class="btn btn-primary" onclick="display_none()">' + \
                      '<span class="glyphicon glyphicon-arrow-left" aria-hidden="true"></span>Try Again' + \
                      '</button>'

    html_alertState = '<div id="alertState" class="col-md-11"><div class="form-group alert ' + alert_type + '" role="alert">' + \
                      '<h4 class="alert-heading">' + msg_head + '</h4>' + \
                      '<p>' + msg_content + '</p>' + \
                      '<hr>' + \
                      '<p class="mb-0">' + msg_info + '</p>' + \
                      '</div>' + \
                      '<div class="form-group">' + button_html + '</div></div>'
    visibility = '"none"'

    return html_alertState, visibility, return_val, thread_function


def delete_plugin(plugin):
    old_path = plugin.location
    user_folder, plugin_folder = os.path.split(old_path)
    deleted_plugins_path = os.path.join(user_folder, "__deleted")
    os.makedirs(deleted_plugins_path, exist_ok=True)
    ok = os.system(f"mv {old_path} {deleted_plugins_path}")
    if ok == 0:
        return os.path.join(deleted_plugins_path, plugin_folder)
    else:
        return False


def ini2json(ini):
    try:
        cfg = configparser.ConfigParser()
        config = {}

        cfg.read_string(ini)
        for section in cfg.sections():
            config[section] = {}
            for name, value in cfg.items(section):
                config[section][name] = [x.strip() for x in value.split() if x]
                if len(config[section][name]) == 1:
                    config[section][name] = config[section][name][0]
                elif len(config[section][name]) == 0:
                    config[section][name] = ''

        return json.dumps(config)
    except:

        return None
