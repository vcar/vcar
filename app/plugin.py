from flask import current_app
from flask_plugins import Plugin


class AppPlugin(Plugin):

    """ Custom plugin class, it implements some useful methods
        to deal with plugins
    """

    has_settings = False

    def register_blueprint(self, blueprint, **kwargs):
        """Register a plugin blueprint"""
        current_app.register_blueprint(blueprint, **kwargs)

    def is_installed(self):
        """Check whether the plugin is installed"""
        return self.has_settings is True

    def is_enabled(self):
        """Check whether the plugin is enabled"""
        return self.has_settings is True

    def uninstallable(self):
        """Check whether the plugin is installed and can be uninstalled"""
        return self.has_settings is True

    def enabled(self):
        """Enable plugin"""
        return self.has_settings is True

    def disable(self):
        """Disable plugin"""
        return self.has_settings is True

    @staticmethod
    def all(self):
        """List all plugin"""
        return True

    @staticmethod
    def all_enabled(self):
        """List all enabled plugin"""
        return True

    @staticmethod
    def all_disabled(self):
        """List all disabled plugin"""
        return True
