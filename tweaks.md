Hello,

Here is some tweaks to be done for installed packages:


Flask-plugin
	File   : venv/lib/python2.7/site-packages/flask_plugins/__init__.py
	Change : 241
		base_plugin_folder = self.plugin_folder.split(os.sep)[-1]
        self.base_plugin_package = ".".join(
            [base_app_folder, base_plugin_folder]
        )