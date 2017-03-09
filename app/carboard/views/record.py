from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import login_required

from . import carboard
from ..models.record import Record
from ..models.user import User
from ..models.drivetype import DriveType
from ..models.vehicle import Vehicle
from ..models.driver import Driver
from ..models.status import Status
from ..forms.record import RecordForm, RecordStatusForm
from ..helpers import paginate, choices, upload_file
from ..constants import PER_PAGE, DRIVE_FILES_DIR
from ...extensions import db

# --------------------- /carboard/record/ : List of records ------------------ #

@carboard.route('/record/')
@login_required
def indexRecord():
    records = Record.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    return render_template('carboard/record/index.html', records=records)

# ----------------------- /carboard/record/id : Show record ------------------- #


@carboard.route('/record/<int:id>', methods=['GET'])
@login_required
def showRecord(id):
    record = Record.query.get_or_404(id)
    return render_template('carboard/record/show.html', record=record)

# ---------------------- /carboard/record/new : Add record -------------------- #


@carboard.route('/record/new', methods=['GET', 'POST'])
@login_required
def newRecord():
    """ Add new record """

    form = RecordForm()
    form.user_id.choices = choices(User, 'Select a user', 1, 'username')
    form.drivetype_id.choices = choices(DriveType, 'Select a drive type', False)
    form.driver_id.choices = choices(Driver, 'Select a Driver', False, 'fullname')
    form.vehicle_id.choices = choices(Vehicle, 'Select a vehicle', False, 'id')

    if form.validate_on_submit():
        trace = upload_file(form.trace.data, DRIVE_FILES_DIR)
        record = Record(
            user_id=form.user_id.data,
            drivetype_id=form.drivetype_id.data,
            driver_id=form.driver_id.data,
            vehicle_id=form.vehicle_id.data,
            name=form.name.data,
            start=form.start.data,
            end=form.end.data,
            description=form.description.data,
            trace=trace
        )
        db.session.add(record)
        db.session.commit()
        flash('Record {}, added successfully.'.format(record.name), 'success')
        return redirect(url_for('carboard.indexRecord'))

    return render_template('carboard/record/new.html', form=form)

# -------------------- /carboard/record/id/edit : Edit record ----------------- #


@carboard.route('/record/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editRecord(id):
    """ Edit existing record """
    record = Record.query.get_or_404(id)
    oldTrace = record.trace

    form = RecordForm(obj=record)
    del form.trace
    form.user_id.choices = choices(User, 'Select a user', 1, 'username')
    form.drivetype_id.choices = choices(DriveType, 'Select a drive type', False)
    form.driver_id.choices = choices(Driver, 'Select a Driver', False, 'fullname')
    form.vehicle_id.choices = choices(Vehicle, 'Select a vehicle', False, 'id')

    if form.validate_on_submit():
        form.populate_obj(record)
        db.session.commit()
        flash('Record {}, updated successfully.'.format(record.name), 'success')
        return redirect(url_for('carboard.showRecord', id=id))

    return render_template('carboard/record/edit.html', form=form, id=id)

# ------------------ /carboard/record/id/delete : Delete record --------------- #


@carboard.route('/record/<int:id>/toggle', methods=['GET', 'POST'])
@login_required
def toggleRecord(id):
    record = Record.query.get_or_404(id)
    form = RecordStatusForm(obj=record)
    form.status_id.choices = [(s.id, s) for s in Status.query.all()]
    if form.validate_on_submit():
        form.populate_obj(record)
        db.session.commit()
        flash('Record {}, updated successfully.'.format(record.name), 'success')
        return redirect(url_for('carboard.showRecord', id=id))
    return render_template('carboard/record/status.html', form=form, id=id)

# ------------------ /carboard/record/id/delete : Delete record --------------- #


@carboard.route('/record/<int:id>/delete', methods=['GET'])
@login_required
def deleteRecord(id):
    record = Record.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    flash('Record {}, deleted successfully.'.format(record.name), 'success')
    return redirect(url_for('carboard.indexRecord'))
