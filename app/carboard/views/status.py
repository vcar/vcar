from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import login_required

from . import carboard
from ..models.status import Status
from ..forms.status import StatusForm
from ..helpers import paginate
from ..constants import PER_PAGE
from ...extensions import db


# --------------------- /carboard/status/ : List of countries ------------------ #

@carboard.route('/status/')
@login_required
def indexStatus():
    status = Status.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    return render_template('carboard/status/index.html',
                           status=status
                           )

# ----------------------- /carboard/status/id : Show status ------------------- #


@carboard.route('/status/<int:id>', methods=['GET'])
@login_required
def showStatus(id):
    status = Status.query.get_or_404(id)
    return render_template('carboard/status/show.html',
                           status=status
                           )

# ---------------------- /carboard/status/new : Add status -------------------- #


@carboard.route('/status/new', methods=['GET', 'POST'])
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
        return redirect(url_for('carboard.indexStatus'))

    return render_template('carboard/status/new.html', form=form)

# -------------------- /carboard/status/id/edit : Edit status ----------------- #


@carboard.route('/status/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editStatus(id):
    """ Edit existing status """
    status = Status.query.get_or_404(id)
    form = StatusForm(obj=status)
    if form.validate_on_submit():
        form.populate_obj(status)
        db.session.commit()
        flash('Status {}, updated successfully.'.format(form.title.data), 'success')
        return redirect(url_for('carboard.showStatus', id=id))

    return render_template('carboard/status/edit.html', form=form, id=id)

# ------------------ /carboard/status/id/delete : Delete status --------------- #


@carboard.route('/status/<int:id>/delete', methods=['GET'])
@login_required
def deleteStatus(id):
    status = Status.query.get_or_404(id)
    db.session.delete(status)
    db.session.commit()
    flash('Status {}, deleted successfully.'.format(status.title), 'success')
    return redirect(url_for('carboard.indexStatus'))
