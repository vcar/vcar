from app.plugin import AppPlugin
from .src.views import driverGraph

__plugin__ = "DriverGraph"
__version__ = "1.0.0"


class DriverGraph(AppPlugin):

    def setup(self):
        self.register_blueprint(driverGraph)
