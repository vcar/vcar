from flask_script import Manager
from core.main import create_app
from core.extensions import db

import os

app = create_app()
manager = Manager(app)


@manager.command
def run():
    """Run in local machine."""
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(threaded=True, host='0.0.0.0')

if __name__ == "__main__":
    manager.run()
