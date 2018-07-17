from werkzeug.debug import DebuggedApplication
from app import app as application

if application.debug:
        application.wsgi_app = DebuggedApplication(
            application.wsgi_app, evalex=True)

if __name__ == "__main__":
    application.run()
