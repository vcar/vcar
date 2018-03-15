from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import login_required

from . import dashboard
from ..models.drivetype import DriveType
from ..forms.drivetype import DriveTypeForm
from ..helpers.helpers import paginate
from ..constants.constants import PER_PAGE
from ...extensions import db


# --------------------- /dashboard/drivetype/ : List of countries ------------------ #

@dashboard.route('/drivetype/')
@login_required
def indexDriveType():
    drivetypes = DriveType.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    return render_template('dashboard/drivetype/index.html',
                           drivetypes=drivetypes
                           )

# ----------------------- /dashboard/drivetype/id : Show drivetype ------------------- #


@dashboard.route('/drivetype/<int:id>', methods=['GET'])
@login_required
def showDriveType(id):
    drivetype = DriveType.query.get_or_404(id)
    return render_template('dashboard/drivetype/show.html',
                           drivetype=drivetype
                           )

# ---------------------- /dashboard/drivetype/new : Add drivetype -------------------- #


@dashboard.route('/drivetype/new', methods=['GET', 'POST'])
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
        return redirect(url_for('dashboard.indexDriveType'))

    return render_template('dashboard/drivetype/new.html', form=form)

# -------------------- /dashboard/drivetype/id/edit : Edit drivetype ----------------- #


@dashboard.route('/drivetype/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editDriveType(id):
    """ Edit existing driver type """
    drivetype = DriveType.query.get_or_404(id)
    form = DriveTypeForm(obj=drivetype)
    if form.validate_on_submit():
        form.populate_obj(drivetype)
        db.session.commit()
        flash('Driver type {}, updated successfully.'.format(form.name.data), 'success')
        return redirect(url_for('dashboard.showDriveType', id=id))

    return render_template('dashboard/drivetype/edit.html', form=form, id=id)

# ------------------ /dashboard/drivetype/id/delete : Delete drivetype --------------- #


@dashboard.route('/drivetype/<int:id>/delete', methods=['GET'])
@login_required
def deleteDriveType(id):
    drivetype = DriveType.query.get_or_404(id)
    db.session.delete(drivetype)
    db.session.commit()
    flash('Driver type {}, deleted successfully.'.format(drivetype.name), 'success')
    return redirect(url_for('dashboard.indexDriveType'))
