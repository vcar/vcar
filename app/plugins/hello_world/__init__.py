from app.plugin import AppPlugin
from .src.views import hello

__plugin__ = "HelloWorld"
__version__ = "1.0.0"


class HelloWorld(AppPlugin):

    def setup(self):
        self.register_blueprint(hello)
