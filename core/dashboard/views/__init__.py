from flask import render_template
from flask_login import login_required, current_user
from flask import g

from .. import dashboard
from ..models.record import Record
from ..models.vehicle import Vehicle
from ..models.driver import Driver
from ..constants.constants import PER_HOME_PAGE

# --------------------- /dashboard/index : User home page -------------------- #


@dashboard.route('/')
@login_required
def index():
    records = Record.query.order_by(Record.created).limit(PER_HOME_PAGE).all()
    vehicles = Vehicle.query.order_by(Vehicle.created).limit(PER_HOME_PAGE).all()
    drivers = Driver.query.order_by(Driver.created).limit(PER_HOME_PAGE).all()
    return render_template(
        'dashboard/index.html',
        user=current_user,
        records=records,
        vehicles=vehicles,
        drivers=drivers,
    )


@dashboard.route('/configuration')
@login_required
def configuration():
    # may be some logic !
    return render_template('dashboard/elements/configuration.html')
