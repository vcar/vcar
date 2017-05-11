from .config import DefaultConfig

# -------------------------- Sqlalchemy Configuration ----------------------- #


class DatabaseConfig(object):

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SQLALCHEMY_ECHO = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DefaultConfig.INSTANCE_FOLDER_PATH + '/YooNa.db'

    # SQLALCHEMY_DATABASE_URI = 'mysql://user:pass@server/db?charset=utf8'
