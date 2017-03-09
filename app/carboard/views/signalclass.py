from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import login_required

from . import carboard
from ..models.signalclass import Signalclass
from ..forms.signalclass import SignalclassForm
from ..helpers import paginate
from ..constants import PER_PAGE
from ...extensions import db

# --------------------- /carboard/signalclass/ : List of signalclasses ----- #


@carboard.route('/signalclass/')
@login_required
def indexSignalclass():
    signalclasses = Signalclass.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    return render_template('carboard/signalclass/index.html', signalclasses=signalclasses)

# ----------------------- /carboard/signalclass/id : Show signalclass ----- #


@carboard.route('/signalclass/<int:id>', methods=['GET'])
@login_required
def showSignalclass(id):
    signalclass = Signalclass.query.get_or_404(id)
    return render_template('carboard/signalclass/show.html', signalclass=signalclass)

# ---------------------- /carboard/signalclass/new : Add signalclass -------------------- #


@carboard.route('/signalclass/new', methods=['GET', 'POST'])
@login_required
def newSignalclass():
    """ Add new signalclass """
    form = SignalclassForm()
    if form.validate_on_submit():
        signalclass = Signalclass(
            name=form.name.data,
        )
        db.session.add(signalclass)
        db.session.commit()
        flash('Signal class {}, added successfully.'.format(form.name.data), 'success')
        return redirect(url_for('carboard.indexSignalclass'))

    return render_template('carboard/signalclass/new.html', form=form)

# -------------------- /carboard/signalclass/id/edit : Edit signalclass ----------------- #


@carboard.route('/signalclass/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editSignalclass(id):
    """ Edit existing signalclass """
    signalclass = Signalclass.query.get_or_404(id)
    form = SignalclassForm(obj=signalclass)
    if form.validate_on_submit():
        form.populate_obj(signalclass)
        db.session.commit()
        flash('Signal class {}, updated successfully.'.format(form.name.data), 'success')
        return redirect(url_for('carboard.showSignalclass', id=id))

    return render_template('carboard/signalclass/edit.html', form=form, id=id)

# ------------------ /carboard/signalclass/id/delete : Delete signalclass --------------- #


@carboard.route('/signalclass/<int:id>/toggle', methods=['GET'])
@login_required
def toggleSignalclass(id):
    signalclass = Signalclass.query.get_or_404(id)
    status = signalclass.status if signalclass.status is not None else 0
    signalclass.status = 1 - status
    db.session.commit()
    msg = 'activated' if signalclass.status is 1 else 'deactivated'
    flash('Signal class {}, {} successfully.'.format(signalclass.name, msg), 'success')
    return redirect(url_for('carboard.indexSignalclass'))

# ------------------ /carboard/signalclass/id/delete : Delete signalclass --------------- #


@carboard.route('/signalclass/<int:id>/delete', methods=['GET'])
@login_required
def deleteSignalclass(id):
    signalclass = Signalclass.query.get_or_404(id)
    db.session.delete(signalclass)
    db.session.commit()
    flash('Signal class {}, deleted successfully.'.format(signalclass.name), 'success')
    return redirect(url_for('carboard.indexSignalclass'))
