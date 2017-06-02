from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import g

from ..models.record import Record
from ..models.vehicle import Vehicle
from ..models.driver import Driver
from ..constants import PER_HOME_PAGE

carboard = Blueprint('carboard', __name__, url_prefix='/carboard')

from .article import *
from .brand import *
from .country import *
from .dataset import *
from .driver import *
from .drivetype import *
from .extrasignal import *
from .model import *
from .platform import *
from .record import *
from .signal import *
from .signalclass import *
from .signalsource import *
from .status import *
from .user import *
from .vehicle import *
from .plugin import *
# --------------------- /carboard/index : User home page -------------------- #


@carboard.route('/')
@login_required
def index():
    records = Record.query.order_by(Record.created).limit(PER_HOME_PAGE).all()
    vehicles = Vehicle.query.order_by(Vehicle.created).limit(PER_HOME_PAGE).all()
    drivers = Driver.query.order_by(Driver.created).limit(PER_HOME_PAGE).all()
    return render_template(
        'carboard/index.html',
        user=current_user,
        records=records,
        vehicles=vehicles,
        drivers=drivers,
    )


@carboard.route('/configuration')
@login_required
def configuration():
    # may be some logic !
    return render_template('elements/configuration.html')
