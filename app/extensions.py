from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cache import Cache
from flask_mail import Mail
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from flask_images import Images
from flask_redis import FlaskRedis
from flask_plugins import PluginManager
from flask_misaka import Misaka
from flask_socketio import SocketIO
# from flask_session import Session

# ------------------------- Inisialize Database object ---------------------- #

db = SQLAlchemy()

# ------------------------- Inisialize Database object ---------------------- #

migrate = Migrate()

# ------------------------- Inisialize Cache object ------------------------- #

cache = Cache()

# ------------------------- Inisialize Mail object -------------------------- #

mail = Mail()

# ------------------------- Inisialize Login object ------------------------- #

login_manager = LoginManager()

# ------------------------- Inisialize DebugToolbar object ------------------ #

toolbar = DebugToolbarExtension()

# ------------------------- Inisialize Images object ------------------------ #

images = Images()

# ------------------------- Inisialize SocketIO object ---------------------- #

socketio = SocketIO()

# ------------------------- Inisialize Redis object ------------------------- #

redis = FlaskRedis()

# ------------------------- Inisialize PluginManager object ----------------- #

plugin_manager = PluginManager()

# ------------------------- Inisialize Misaka object ----------------- #

misaka = Misaka(tables=True, highlight=True)

# ------------------------- Inisialize Session object ----------------------- #
"""
    Flask-Session save session data on server with many options: filesystem,
    Redis, Sqlite, ...
"""
# session = Session()

# ------------------------------------ X ------------------------------------ #
