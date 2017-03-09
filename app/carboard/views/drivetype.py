from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import login_required

from . import carboard
from ..models.drivetype import DriveType
from ..forms.drivetype import DriveTypeForm
from ..helpers import paginate
from ..constants import PER_PAGE
from ...extensions import db


# --------------------- /carboard/drivetype/ : List of countries ------------------ #

@carboard.route('/drivetype/')
@login_required
def indexDriveType():
    drivetypes = DriveType.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    return render_template('carboard/drivetype/index.html',
                           drivetypes=drivetypes
                           )

# ----------------------- /carboard/drivetype/id : Show drivetype ------------------- #


@carboard.route('/drivetype/<int:id>', methods=['GET'])
@login_required
def showDriveType(id):
    drivetype = DriveType.query.get_or_404(id)
    return render_template('carboard/drivetype/show.html',
                           drivetype=drivetype
                           )

# ---------------------- /carboard/drivetype/new : Add drivetype -------------------- #


@carboard.route('/drivetype/new', methods=['GET', 'POST'])
@login_required
def newDriveType():
    """ Add new driver type """

    form = DriveTypeForm()

    if form.validate_on_submit():
        drivetype = DriveType(
            name=form.name.data
        )
        db.session.add(drivetype)
        db.session.commit()
        flash('Driver type {}, added successfully.'.format(form.name.data), 'success')
        return redirect(url_for('carboard.indexDriveType'))

    return render_template('carboard/drivetype/new.html', form=form)

# -------------------- /carboard/drivetype/id/edit : Edit drivetype ----------------- #


@carboard.route('/drivetype/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editDriveType(id):
    """ Edit existing driver type """
    drivetype = DriveType.query.get_or_404(id)
    form = DriveTypeForm(obj=drivetype)
    if form.validate_on_submit():
        form.populate_obj(drivetype)
        db.session.commit()
        flash('Driver type {}, updated successfully.'.format(form.name.data), 'success')
        return redirect(url_for('carboard.showDriveType', id=id))

    return render_template('carboard/drivetype/edit.html', form=form, id=id)

# ------------------ /carboard/drivetype/id/delete : Delete drivetype --------------- #


@carboard.route('/drivetype/<int:id>/delete', methods=['GET'])
@login_required
def deleteDriveType(id):
    drivetype = DriveType.query.get_or_404(id)
    db.session.delete(drivetype)
    db.session.commit()
    flash('Driver type {}, deleted successfully.'.format(drivetype.name), 'success')
    return redirect(url_for('carboard.indexDriveType'))
