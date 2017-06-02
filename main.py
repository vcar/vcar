from flask import Flask, render_template, g
import flask_plugins

from config.config import DefaultConfig
from config.database import DatabaseConfig
from config.mail import MailConfig

from app.frontend import frontend
from app.carboard import carboard
from app.importer import importer
from app.explorer import explorer
from app.dashboard import dashboard
from app.api import api
from app.filters import filters

from app.carboard.models.user import User
from app.extensions import (
    db, migrate, mail, toolbar, images, login_manager, redis, plugin_manager
    # , cache , session
)


__all__ = ['create_app']

# ----------------------------- Blueprints List ----------------------------- #

DEFAULT_BLUEPRINTS = (
    api,
    frontend,
    carboard,
    dashboard,
    importer,
    explorer,
    filters
)

# ------------------------ Create a flask application ----------------------- #


def create_app(config=None, app_name=None, blueprints=None):
    """Create a flask application."""

    if app_name is None:
        app_name = DefaultConfig.PROJECT
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS
    # Create a flask application instance
    app = Flask(
        app_name,
        # static_url_path='',
        instance_path=DefaultConfig.INSTANCE_FOLDER_PATH,
        instance_relative_config=True
    )
    # jinja configuration
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    # App configuration
    configure_app(app, config)
    # Static configuration
    static_file_status(app)
    # Before request
    configure_hook(app)
    # Register blueprints
    configure_blueprints(app, blueprints)
    # Inisialize extensions
    configure_extensions(app)
    # Template filters
    configure_template_filters(app)
    # Register plugins menu in g
    register_plugins_menu(app)
    # Error handling
    configure_error_handlers(app)

    return app


# --------------------------- Minified static files ------------------------ #

def static_file_status(app, debug=None):
    """Use minified static files if debug is True"""
    if debug is None:
        debug = app.config['DEBUG']
    minified = ".min" if debug is False else ""
    app.jinja_env.globals.update(minified=minified)
    app.jinja_env.add_extension('jinja2.ext.do')

# ----------------------------- App configuration --------------------------- #


def configure_app(app, config=None):
    """App configuration."""

    app.config.from_object(DefaultConfig)
    app.config.from_object(DatabaseConfig)
    app.config.from_object(MailConfig)
    if config:
        app.config.from_object(config)

# ------------------------------- Before & After request -------------------- #


def configure_hook(app):
    @app.before_request
    def before_request():
        pass

    @app.after_request
    def apply_caching(response):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response
# ---------------------------- Register blueprints ------------------------- #


def configure_blueprints(app, blueprints):
    """Configure blueprints in views."""

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

# --------------------------- Inisialize extensions ------------------------ #


def configure_extensions(app):

    # flask-sqlalchemy
    db.init_app(app)

    # flask-migrate
    migrate.init_app(app, db)

    # flask-mail
    mail.init_app(app)
    # flask-cache
    # cache.init_app(app)

    # initialize debug toolbar
    # toolbar.init_app(app)

    # initialize Images utils
    images.init_app(app)

    # initialize FlaskRedis
    redis.init_app(app)

    # initialize SocketIO
    # socketio.init_app(app)

    # initialize Session
    # session.init_app(app)

    # initialize pluginManager
    # plugin_manager.init_app(
    #     app,
    #     base_app_folder='app',
    #     plugin_folder="app/plugins"
    # )
    plugin_manager.init_app(
        app,
        plugin_folder="app/plugins",
        plugin_import_path='app.plugins',
    )

    # flask-login
    login_manager.login_view = 'carboard.login'
    login_manager.refresh_view = 'carboard.reauth'

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)
    login_manager.setup_app(app)

# ------------------------------ Template filters -------------------------- #


def configure_template_filters(app):

    @app.template_filter()
    def pretty_date(value):
        return pretty_date(value)

    @app.template_filter()
    def format_date(value, format='%Y-%m-%d'):
        return value.strftime(format)

# ------------------------------ Plugins menus ----------------------------- #


def convert_keys_to_string(dictionary):
    """Recursively converts dictionary keys to strings."""
    if not isinstance(dictionary, dict):
        return dictionary
    return dict((str(k), str(convert_keys_to_string(v)))
                for k, v in dictionary.items())


def register_plugins_menu(app):

    @app.context_processor
    def configure_plugins_menu():
        plugins = flask_plugins.get_all_plugins()

        plugins_menu = []
        for plugin in plugins:
            if plugin.options['favorite']:
                plugins_menu.append({
                    'id': str(plugin.identifier),
                    'name': str(plugin.name),
                    'favorite': plugin.options['favorite'],
                    'treeview': plugin.options['treeview'],
                    'menu': plugin.options['menu']
                })
        return {'plugins_menu': plugins_menu}

# ------------------------------- Error handling --------------------------- #


def configure_error_handlers(app):

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("errors/forbidden_page.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/page_not_found.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/server_error.html"), 500
