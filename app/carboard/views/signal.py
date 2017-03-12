from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import login_required

from . import carboard
from ..models.signal import Signal
from ..models.signalclass import Signalclass
from ..models.signalsource import Signalsource
from ..forms.signal import SignalForm
from ..helpers import paginate, choices
from ..constants import PER_PAGE
from ...extensions import db

# --------------------- /carboard/signal/ : List of signals ----- #


@carboard.route('/signal/')
@login_required
def indexSignal():
    signals = Signal.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    return render_template('carboard/signal/index.html', signals=signals)

# ----------------------- /carboard/signal/id : Show signal ----- #


@carboard.route('/signal/<int:id>', methods=['GET'])
@login_required
def showSignal(id):
    signal = Signal.query.get_or_404(id)
    return render_template('carboard/signal/show.html', signal=signal)

# ---------------------- /carboard/signal/new : Add signal -------------------- #


@carboard.route('/signal/new', methods=['GET', 'POST'])
@login_required
def newSignal():
    """ Add new signal """
    form = SignalForm()
    form.signalclass_id.choices = choices(Signalclass, 'Select signal class', 1)
    form.signalsource_id.choices = choices(Signalsource, 'Select signal source', 1)
    if form.validate_on_submit():
        signal = Signal(
            name=form.name.data,
            signalclass_id=form.signalclass_id.data,
            signalsource_id=form.signalsource_id.data,
        )
        db.session.add(signal)
        db.session.commit()
        flash('Signal {}, added successfully.'.format(form.name.data), 'success')
        return redirect(url_for('carboard.indexSignal'))

    return render_template('carboard/signal/new.html', form=form)

# -------------------- /carboard/signal/id/edit : Edit signal ----------------- #


@carboard.route('/signal/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editSignal(id):
    """ Edit existing signal """
    signal = Signal.query.get_or_404(id)
    form = SignalForm(obj=signal)
    form.signalclass_id.choices = choices(Signalclass, 'Select signal class', 1)
    form.signalsource_id.choices = choices(Signalsource, 'Select signal source', 1)
    if form.validate_on_submit():
        form.populate_obj(signal)
        db.session.commit()
        flash('Signal {}, updated successfully.'.format(form.name.data), 'success')
        return redirect(url_for('carboard.showSignal', id=id))

    return render_template('carboard/signal/edit.html', form=form, id=id)

# ------------------ /carboard/signal/id/delete : Delete signal --------------- #


@carboard.route('/signal/<int:id>/toggle', methods=['GET'])
@login_required
def toggleSignal(id):
    signal = Signal.query.get_or_404(id)
    status = signal.status if signal.status is not None else 0
    signal.status = 1 - status
    db.session.commit()
    msg = 'activated' if signal.status is 1 else 'deactivated'
    flash('Signal {}, {} successfully.'.format(signal.name, msg), 'success')
    return redirect(url_for('carboard.indexSignal'))

# ------------------ /carboard/signal/id/delete : Delete signal --------------- #


@carboard.route('/signal/<int:id>/delete', methods=['GET'])
@login_required
def deleteSignal(id):
    signal = Signal.query.get_or_404(id)
    db.session.delete(signal)
    db.session.commit()
    flash('Signal {}, deleted successfully.'.format(signal.name), 'success')
    return redirect(url_for('carboard.indexSignal'))
