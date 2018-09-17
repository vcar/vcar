import os


# --------------------------- Default Configuration ------------------------- #
class DefaultConfig(object):
    # Project name
    PROJECT = "vCar"
    # project version
    VERSION = "0.1.8"
    # Turns on debugging features in Flask
    ENV = "DEVELOPMENT"
    # Turns on debugging features in Flask
    DEBUG = True
    # Disabling the Werkzeug PIN Confirmation
    WERKZEUG_DEBUG_PIN = 'off'
    # secret key
    SECRET_KEY = "Zfe&45f4y5fhgse6f4e&@+-%_r4oij5hgfa&#@"
    # Redis database url
    REDIS_URL = "redis://:password@localhost:6379/0"
    # Flask Session type
    SESSION_TYPE = 'filesystem'
    # Configuration for the Flask-Bcrypt extension
    BCRYPT_LEVEL = 12
    # Application root directory
    APP_ROOT = os.path.dirname(os.path.abspath('.'))
    # Application email
    MAIL_FROM_EMAIL = "misaki.yooko@gmail.com"
    # Upload directory
    UPLOAD_DIR = "static/uploads/"
    # Avater upload directory
    UPLOAD_AVATAR_DIR = os.path.join(UPLOAD_DIR, 'avatars/')
    ALLOWED_AVATAR_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    IMAGES_URL = "/dashboard/imgsizer"
    IMAGES_PATH = ['core/dashboard/static']
    # IMAGES_CACHE = "/tmp/flask-images"
    # Instance folder path
    INSTANCE_FOLDER_PATH = os.path.join(os.path.abspath('.'), 'instance')
    # INSTANCE_FOLDER_PATH = os.path.join('/home/karim/OpenXC/Dashboard/Flask/instance')
    # INSTANCE_FOLDER_PATH = os.path.join('I:/home/karim/OpenXC/Dashboard/Flask', 'instance')
    UPLOAD_USER = "uploads/avatars/"
    UPLOAD_BRAND = "uploads/brands/"
    UPLOAD_DRIVER = "uploads/drivers/"
    UPLOAD_VEHICLE = "uploads/vehicles/"
    UPLOAD_RECORDS = "uploads/records/"
    UPLOAD_PLATFORM = "uploads/platforms/"
    # Cache configuration
    CACHE_TYPE = 'null'
    CACHE_DEFAULT_TIMEOUT = 1
    TEMPLATES_AUTO_RELOAD = True
    # ToolbarExtention Configuration
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True
    DEBUG_TB_PROFILER_ENABLED = True


# ---------------------------- Debug Configuration -------------------------- #


class DebugConfig(DefaultConfig):
    # Turns on debugging features in Flask
    DEBUG = True
    # secret key
    SECRET_KEY = "devlopement key"
    # Avater upload directory
    UPLOAD_AVATAR_DIR = "static/uploads/avatars/"
    # Instance folder path
    INSTANCE_FOLDER_PATH = os.path.join('/tmp', 'instance')
    # Cache configuration
    CACHE_TYPE = 'null'
    CACHE_DEFAULT_TIMEOUT = 60
