from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cache import Cache
from flask_mail import Mail
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from flask_socketio import SocketIO
from flask_images import Images
from flask_session import Session

# ------------------------ Inisialize Database object ----------------------- #

db = SQLAlchemy()

# ------------------------ Inisialize Database object ----------------------- #

migrate = Migrate()

# ------------------------- Inisialize Cache object ------------------------- #

cache = Cache()

# -------------------------- Inisialize Mail object ------------------------- #

mail = Mail()

# ------------------------- Inisialize Login object ------------------------- #

login_manager = LoginManager()

# ---------------------- Inisialize DebugToolbar object --------------------- #

toolbar = DebugToolbarExtension()

# ------------------------- Inisialize Images object ------------------------ #

images = Images()

# ------------------------ Inisialize SocketIO object ----------------------- #

# socketio = SocketIO()

# ------------------------ Inisialize Session object ----------------------- #
"""
	Flask-Session save session data on server with many options: filesystem,
	Redis, Sqlite, ...
"""
# session = Session()

# ------------------------------------ X ------------------------------------ #
