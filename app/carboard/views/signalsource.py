from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import login_required

from . import carboard
from ..models.signalsource import Signalsource
from ..forms.signalsource import SignalsourceForm
from ..helpers import paginate
from ..constants import PER_PAGE
from ...extensions import db

# --------------------- /carboard/signalsource/ : List of signalsources ----- #


@carboard.route('/signalsource/')
@login_required
def indexSignalsource():
    signalsources = Signalsource.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    return render_template('carboard/signalsource/index.html', signalsources=signalsources)

# ----------------------- /carboard/signalsource/id : Show signalsource ----- #


@carboard.route('/signalsource/<int:id>', methods=['GET'])
@login_required
def showSignalsource(id):
    signalsource = Signalsource.query.get_or_404(id)
    return render_template('carboard/signalsource/show.html', signalsource=signalsource)

# ---------------------- /carboard/signalsource/new : Add signalsource -------------------- #


@carboard.route('/signalsource/new', methods=['GET', 'POST'])
@login_required
def newSignalsource():
    """ Add new signalsource """
    form = SignalsourceForm()
    if form.validate_on_submit():
        signalsource = Signalsource(
            name=form.name.data,
        )
        db.session.add(signalsource)
        db.session.commit()
        flash('Signal source {}, added successfully.'.format(form.name.data), 'success')
        return redirect(url_for('carboard.indexSignalsource'))

    return render_template('carboard/signalsource/new.html', form=form)

# -------------------- /carboard/signalsource/id/edit : Edit signalsource ----------------- #


@carboard.route('/signalsource/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editSignalsource(id):
    """ Edit existing signalsource """
    signalsource = Signalsource.query.get_or_404(id)
    form = SignalsourceForm(obj=signalsource)
    if form.validate_on_submit():
        form.populate_obj(signalsource)
        db.session.commit()
        flash('Signal source {}, updated successfully.'.format(form.name.data), 'success')
        return redirect(url_for('carboard.showSignalsource', id=id))

    return render_template('carboard/signalsource/edit.html', form=form, id=id)

# ------------------ /carboard/signalsource/id/delete : Delete signalsource --------------- #


@carboard.route('/signalsource/<int:id>/toggle', methods=['GET'])
@login_required
def toggleSignalsource(id):
    signalsource = Signalsource.query.get_or_404(id)
    status = signalsource.status if signalsource.status is not None else 0
    signalsource.status = 1 - status
    db.session.commit()
    msg = 'activated' if signalsource.status is 1 else 'deactivated'
    flash('Signal source {}, {} successfully.'.format(signalsource.name, msg), 'success')
    return redirect(url_for('carboard.indexSignalsource'))

# ------------------ /carboard/signalsource/id/delete : Delete signalsource --------------- #


@carboard.route('/signalsource/<int:id>/delete', methods=['GET'])
@login_required
def deleteSignalsource(id):
    signalsource = Signalsource.query.get_or_404(id)
    db.session.delete(signalsource)
    db.session.commit()
    flash('Signal source {}, deleted successfully.'.format(signalsource.name), 'success')
    return redirect(url_for('carboard.indexSignalsource'))
