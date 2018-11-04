from datetime import datetime

from flask_login import current_user

from ..helpers.helpers import slugify
from ...extensions import db


# -------------------------------- Plugin Model ------------------------------- #

class Plugin(db.Model):
    """Plugin Model."""
    __tablename__ = 'plugins'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    identifier = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    description = db.Column(db.String(255))
    location = db.Column(db.Text)
    info = db.Column(db.Text)
    init = db.Column(db.Text)
    options = db.Column(db.Text)
    version = db.Column(db.String(255))
    status = db.Column(db.SmallInteger, default=1)
    created = db.Column(db.DateTime(), default=datetime.utcnow())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')

    def __init__(self, name, **kwargs):
        """
        Initialise a plugin instance
        :param name:
        :param kwargs:
        """
        self.name = name
        self.identifier = slugify(name, '_')
        self.logo = kwargs.get('logo', None)
        self.description = kwargs.get('description', None)
        self.info = kwargs.get('info', None)
        self.init = kwargs.get('init', None)
        self.location = kwargs.get('location', None)
        self.user_id = current_user.id
        self.options = kwargs.get('options', None)
        self.version = kwargs.get('version', None)
        self.status = kwargs.get('status', 1)

    def __repr__(self):
        return f"{self.name} ({self.identifier})"

    def __str__(self):
        return f"{self.name}"


"""
    info = {
        'identifier': 'yoona',
        "name": "Driver Graph",
        "author": "boubouhkarim",
        "license": "BSD",
        "description": "Generate driver behavoir graph.",
        "version": "1.3.6",
    }
    init = {
        "program": root@yoona,
        "user": "karim",
        "type": "core", # community
        "plugin_dir": "@vcar/plugins/core/yoona/"
        "env_dir": "@vcar/plugins/core/yoona/workspace/.env/
        "directory": "/home/karim/Workspace/github.com/vcar/vcar",
        "command": "/home/karim/Workspace/github.com/vcar/.env/bin/gunicorn --workers 1 --bind unix:app.sock --reload wsgi",
        "stderr_logfile": "/var/log/vcar/vcar.err.log",
        "stderr_logfile_maxbytes": 10MB,
        "stdout_logfile": "/var/log/vcar/vcar.out.log",
        "stdout_logfile_maxbytes": "10MB",
    }
    options = {
        "favorite": true,
        "treeview": true,
        "menu": [
            {
                "name": "Overview",
                "action": "driverGraph.index",
                "iclass": "fa fa-flask"
            },
            {
                "name": "Data Sets",
                "action": "driverGraph.datasets",
                "iclass": "fa fa-tachometer"
            },
            {
                "name": "Run",
                "action": "driverGraph.run",
                "iclass": "fa fa-check-circle"
            },
            {
                "name": "Custom",
                "action": "driverGraph.custom",
                "iclass": "fa fa-check-circle"
            },
            {
                "name": "Documentation",
                "action": "driverGraph.docs",
                "iclass": "fa fa-book"
            }
        ]
    }

[program:vcar@dashboard]

user=karim
autostart=true
autorestart=true

directory=/home/karim/Workspace/github.com/vcar/vcar
command=/home/karim/Workspace/github.com/vcar/.env/bin/gunicorn --workers 1 --bind unix:app.sock --reload wsgi


stderr_logfile=/var/log/vcar/vcar.err.log
stderr_logfile_maxbytes=10MB
stdout_logfile=/var/log/vcar/vcar.out.log
stdout_logfile_maxbytes=10MB
"""
