from flask import Blueprint

dashboard = Blueprint(
    'dashboard',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/dashboard'
)

from .views import *
from .views.article import *
from .views.brand import *
from .views.country import *
from .views.dataset import *
from .views.driver import *
from .views.drivetype import *
from .views.extrasignal import *
from .views.importer import *
from .views.model import *
from .views.platform import *
from .views.record import *
from .views.signal import *
from .views.signalclass import *
from .views.signalsource import *
from .views.status import *
from .views.user import *
from .views.vehicle import *
from .views.plugin import *

from . import CreateNewPlugin