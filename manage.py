from flask_script import Manager
from flask_migrate import MigrateCommand
from main import create_app
from app.extensions import db
from app.carboard.models.user import User

import os

app = create_app()
manager = Manager(app)


@manager.command
def run():
    """Run in local machine."""
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Extrafiles are just used to track changer in template folder
    # thus our application is forced to reload.
    extra_dirs = [
        '/home/karim/OpenXC/Dashboard/Flask/vcar/templates',
    ]
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in os.walk(extra_dir):
            for filename in files:
                filename = os.path.join(dirname, filename)
                if os.path.isfile(filename):
                    extra_files.append(filename)

    """
        Get informed : Flask development server can handle only one request :)
            * processes = x   : allow x processes (forks) means x clients
                                Windows sorry you can't fork :)
            * threaded = Bool : allow or not multiple threads.
    """
    # app.run(processes=4, extra_files=extra_files)
    app.run(threaded=True, extra_files=extra_files)
    # app.run(extra_files=extra_files)


@manager.command
def initdb():
    """Init/reset database."""

    # db.drop_all()
    # db.create_all()

    admin = User(
        fullname="Misaki Yooko",
        username="root",
        email="misaki.yooko@gmail.com",
        password='root'
    )

    db.session.add(admin)
    db.session.commit()


# manager.add_option(
#     '-c', '--config',
#     dest="config",
#     required=False,
#     help="config file"
# )
manager.add_command(
    'db',
    MigrateCommand
)

if __name__ == "__main__":
    manager.run()
