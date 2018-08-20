def config_template(plugin_name, user_name, abs_path="/Users/salaheddine/Desktop/vcar_repository/"):
	return """[program:"""+plugin_name+"""-c]
user="""+user_name+"""
directory="""+abs_path+"""vcar/plugins/community/"""+user_name+"""/"""+plugin_name+"""/services
command="""+abs_path+"""vcar/plugins/community/"""+user_name+"""/"""+plugin_name+"""/workspace/.env/bin/gunicorn --bind unix:app.sock --reload wsgi
; -e SCRIPT_NAME=/plugins/community/"""+user_name+"""/"""+plugin_name+"""/ 
autostart=true
autorestart=true

stderr_logfile=/usr/local/var/log/vcar/"""+plugin_name+"""/"""+plugin_name+""".err.log
stderr_logfile_maxbytes=2MB
stdout_logfile=/usr/local/var/log/vcar/"""+plugin_name+"""/"""+plugin_name+""".out.log
stdout_logfile_maxbytes=2MB"""