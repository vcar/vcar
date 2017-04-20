from flask_plugins import connect_event
from app.plugin import AppPlugin

from .src import hello
from .src.views import (
    hello_world, hello_world2,
    inject_hello_world, inject_hello_world2
)

__plugin__ = "HelloWorld"
__version__ = "1.0.0"


class HelloWorld(AppPlugin):
    def setup(self):
        self.register_blueprint(hello, url_prefix="/hello")

        connect_event("after_navigation", hello_world)
        connect_event("after_navigation", hello_world2)

        connect_event("tmpl_before_content", inject_hello_world)
        connect_event("tmpl_before_content", inject_hello_world2)
