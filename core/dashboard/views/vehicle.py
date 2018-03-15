from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import login_required

from . import dashboard
from ..models.vehicle import Vehicle
from ..models.user import User
from ..models.brand import Brand
from ..models.model import Model
from ..models.driver import Driver
from ..models.status import Status
from ..forms.vehicle import VehicleForm, VehicleStatusForm
from ..helpers.helpers import paginate, choices, upload_file
from ..constants.constants import PER_PAGE, VEHICLE_LOGO_DIR
from ...extensions import db

# --------------------- /dashboard/vehicle/ : List of vehicles ------------------ #

@dashboard.route('/vehicle/')
@login_required
def indexVehicle():
    vehicles = Vehicle.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    return render_template('dashboard/vehicle/index.html', vehicles=vehicles)

# ----------------------- /dashboard/vehicle/id : Show vehicle ------------------- #


@dashboard.route('/vehicle/<int:id>', methods=['GET'])
@login_required
def showVehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    return render_template('dashboard/vehicle/show.html', vehicle=vehicle)

# ---------------------- /dashboard/vehicle/new : Add vehicle -------------------- #


@dashboard.route('/vehicle/new', methods=['GET', 'POST'])
@login_required
def newVehicle():
    """ Add new vehicle """

    form = VehicleForm()
    form.user_id.choices = choices(User, 'Select a user', 1, 'username')
    form.brand_id.choices = choices(Brand, 'Select a brand')
    form.model_id.choices = choices(Model, 'Select a model')
    form.driver_id.choices = choices(Driver, 'Select a Driver', False, 'fullname')

    if form.validate_on_submit():
        image = upload_file(form.image.data, VEHICLE_LOGO_DIR)
        vehicle = Vehicle(
            user_id=form.user_id.data,
            brand_id=form.brand_id.data,
            model_id=form.model_id.data,
            driver_id=form.driver_id.data,
            image=image
        )
        db.session.add(vehicle)
        db.session.commit()
        flash('Vehicle {}, added successfully.'.format(vehicle), 'success')
        return redirect(url_for('dashboard.indexVehicle'))

    return render_template('dashboard/vehicle/new.html', form=form)

# -------------------- /dashboard/vehicle/id/edit : Edit vehicle ----------------- #


@dashboard.route('/vehicle/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editVehicle(id):
    """ Edit existing vehicle """
    vehicle = Vehicle.query.get_or_404(id)
    oldImage = vehicle.image

    form = VehicleForm(obj=vehicle)
    form.user_id.choices = choices(User, 'Select a user', 1, 'username')
    form.brand_id.choices = choices(Brand, 'Select a brand')
    form.model_id.choices = choices(Model, 'Select a model')
    form.driver_id.choices = choices(Driver, 'Select a Driver', False, 'fullname')

    if form.validate_on_submit():
        form.populate_obj(vehicle)
        image = upload_file(form.image.data, VEHICLE_LOGO_DIR)
        if image is None:
            vehicle.image = oldImage
        else:
            vehicle.image = image
        db.session.commit()
        flash('Vehicle {}, updated successfully.'.format(vehicle), 'success')
        return redirect(url_for('dashboard.showVehicle', id=id))

    return render_template('dashboard/vehicle/edit.html', form=form, id=id)

# ------------------ /dashboard/vehicle/id/delete : Delete vehicle --------------- #


@dashboard.route('/vehicle/<int:id>/toggle', methods=['GET', 'POST'])
@login_required
def toggleVehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    form = VehicleStatusForm(obj=vehicle)
    form.status_id.choices = [(s.id, s) for s in Status.query.all()]
    if form.validate_on_submit():
        form.populate_obj(vehicle)
        db.session.commit()
        flash('Vehicle {}, updated successfully.'.format(vehicle.brand), 'success')
        return redirect(url_for('dashboard.showVehicle', id=id))
    return render_template('dashboard/vehicle/status.html', form=form, id=id)

# ------------------ /dashboard/vehicle/id/delete : Delete vehicle --------------- #


@dashboard.route('/vehicle/<int:id>/delete', methods=['GET'])
@login_required
def deleteVehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    db.session.delete(vehicle)
    db.session.commit()
    flash('Vehicle {}, deleted successfully.'.format(vehicle), 'success')
    return redirect(url_for('dashboard.indexVehicle'))
