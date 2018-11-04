import os
from core.config.config import DebugConfig

def config_template(plugin_name, user_name, abs_path=None):
    if abs_path is None:
        abs_path = os.path.abspath(".")

    return """
[program:""" + plugin_name + """-c]
user=""" + user_name + """
directory=""" + abs_path + """/plugins/community/""" + user_name + """/""" + plugin_name + """/services
command=""" + abs_path + """/plugins/community/""" + user_name + """/""" + plugin_name + """/workspace/.env/bin/gunicorn --bind unix:app.sock --reload wsgi
; -e SCRIPT_NAME=/plugins/community/""" + user_name + """/""" + plugin_name + """/ 
autostart=true
autorestart=true

stderr_logfile= """ + DebugConfig.PLUGIN_LOG_ROOT_FOLDER + """/""" + plugin_name + """/""" + plugin_name + """.err.log
stderr_logfile_maxbytes=2MB
stdout_logfile= """ + DebugConfig.PLUGIN_LOG_ROOT_FOLDER + """/""" + plugin_name + """/""" + plugin_name + """.out.log
stdout_logfile_maxbytes=2MB"""
