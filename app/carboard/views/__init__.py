from flask import Blueprint, render_template
from flask_login import login_required, current_user

from ..models.record import Record
from ..models.vehicle import Vehicle
from ..models.driver import Driver
from ..constants import PER_HOME_PAGE

carboard = Blueprint('carboard', __name__, url_prefix='/carboard')

from brand import *
from country import *
from driver import *
from drivetype import *
from user import *
from model import *
from status import *
from vehicle import *
from record import *
from platform import *
from signal import *
from extrasignal import *
from signalclass import *
from dataset import *
from article import *
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
