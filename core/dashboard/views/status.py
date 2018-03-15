from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import login_required

from . import dashboard
from ..models.status import Status
from ..forms.status import StatusForm
from ..helpers.helpers import paginate
from ..constants.constants import PER_PAGE
from ...extensions import db


# --------------------- /dashboard/status/ : List of countries ------------------ #

@dashboard.route('/status/')
@login_required
def indexStatus():
    status = Status.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    return render_template('dashboard/status/index.html',
                           status=status
                           )

# ----------------------- /dashboard/status/id : Show status ------------------- #


@dashboard.route('/status/<int:id>', methods=['GET'])
@login_required
def showStatus(id):
    status = Status.query.get_or_404(id)
    return render_template('dashboard/status/show.html',
                           status=status
                           )

# ---------------------- /dashboard/status/new : Add status -------------------- #


@dashboard.route('/status/new', methods=['GET', 'POST'])
@login_required
def newStatus():
    """ Add new status """

    form = StatusForm()

    if form.validate_on_submit():
        status = Status(
            title=form.title.data,
            color=form.color.data
        )
        db.session.add(status)
        db.session.commit()
        flash('Status {}, added successfully.'.format(form.title.data), 'success')
        return redirect(url_for('dashboard.indexStatus'))

    return render_template('dashboard/status/new.html', form=form)

# -------------------- /dashboard/status/id/edit : Edit status ----------------- #


@dashboard.route('/status/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editStatus(id):
    """ Edit existing status """
    status = Status.query.get_or_404(id)
    form = StatusForm(obj=status)
    if form.validate_on_submit():
        form.populate_obj(status)
        db.session.commit()
        flash('Status {}, updated successfully.'.format(form.title.data), 'success')
        return redirect(url_for('dashboard.showStatus', id=id))

    return render_template('dashboard/status/edit.html', form=form, id=id)

# ------------------ /dashboard/status/id/delete : Delete status --------------- #


@dashboard.route('/status/<int:id>/delete', methods=['GET'])
@login_required
def deleteStatus(id):
    status = Status.query.get_or_404(id)
    db.session.delete(status)
    db.session.commit()
    flash('Status {}, deleted successfully.'.format(status.title), 'success')
    return redirect(url_for('dashboard.indexStatus'))
