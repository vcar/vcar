import pprint
from werkzeug.debug import DebuggedApplication
from core.main import create_app

application = create_app()

# Enable Flask Interactive Debugger in Development
if application.debug:
    application.wsgi_app = DebuggedApplication(
        application.wsgi_app, evalex=True, pin_security=False, pin_logging=False
    )

if __name__ == "__main__":
    application.run()


# mode d'affichage plugin
#     Plugin
        
#         Hello world
# ----------------------------------------
# mode d'affichage platform
#     vcar_layout
#     |_________________________________
#     |   |-----------------------------
#     |   |
#     |   |       Hello world
#     |   |




# Core/
#   USER/ [Community]
#     plugin_name/
#         services/
#             internal_folder/..
#             app.py
#             app.sock
#             wsgi.py
#         views/
#             view_name/
#                 index.html
#                 ...
#         workspace/
#             .env/
#             config/
#                 init.conf
#             /exe
#             /tmp
#         /docs
#         license
#         readMe
#         Authors
#         info.js
#         requirement