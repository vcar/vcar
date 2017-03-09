from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import login_required

from . import carboard
from ..models.extrasignal import Extrasignal
from ..models.signal import Signal
from ..models.platform import Platform
from ..forms.extrasignal import ExtrasignalForm
from ..helpers import paginate, choices
from ..constants import PER_PAGE
from ...extensions import db

# --------------------- /carboard/extrasignal/ : List of extrasignals ------------- #

@carboard.route('/extrasignal/')
@login_required
def indexExtrasignal():
    extrasignals = Extrasignal.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    return render_template('carboard/extrasignal/index.html', extrasignals=extrasignals)

# ----------------------- /carboard/extrasignal/id : Show extrasignal ------------------- #


@carboard.route('/extrasignal/<int:id>', methods=['GET'])
@login_required
def showExtrasignal(id):
    extrasignal = Extrasignal.query.get_or_404(id)
    return render_template('carboard/extrasignal/show.html', extrasignal=extrasignal)

# ---------------------- /carboard/extrasignal/new : Add extrasignal -------------------- #


@carboard.route('/extrasignal/new', methods=['GET', 'POST'])
@login_required
def newExtrasignal():
    """ Add new extrasignal """

    form = ExtrasignalForm()
    form.signal_id.choices = choices(Signal, 'Select main signal', 1)
    form.platform_id.choices = choices(Platform, 'Select a platform', 1, 'name')

    if form.validate_on_submit():
        extrasignal = Extrasignal(
            name=form.name.data,
            signal_id=form.signal_id.data,
            platform_id=form.platform_id.data,
        )
        db.session.add(extrasignal)
        db.session.commit()
        flash('Extra signal {}, added successfully.'.format(form.name.data), 'success')
        return redirect(url_for('carboard.indexExtrasignal'))

    return render_template('carboard/extrasignal/new.html', form=form)

# -------------------- /carboard/extrasignal/id/edit : Edit extrasignal ----------------- #


@carboard.route('/extrasignal/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editExtrasignal(id):
    """ Edit existing extrasignal """
    extrasignal = Extrasignal.query.get_or_404(id)
    form = ExtrasignalForm(obj=extrasignal)
    form.signal_id.choices = choices(Signal, 'Select main signal', 1)
    form.platform_id.choices = choices(Platform, 'Select a platform', 1, 'name')

    if form.validate_on_submit():
        form.populate_obj(extrasignal)
        flash('Extra signal {}, updated successfully.'.format(form.name.data), 'success')
        return redirect(url_for('carboard.showExtrasignal', id=id))

    return render_template('carboard/extrasignal/edit.html', form=form, id=id)

# ------------------ /carboard/extrasignal/id/delete : Delete extrasignal --------------- #


@carboard.route('/extrasignal/<int:id>/toggle', methods=['GET'])
@login_required
def toggleExtrasignal(id):
    extrasignal = Extrasignal.query.get_or_404(id)
    # getattr(extrasignal, 'status', 0)
    status = extrasignal.status if extrasignal.status is not None else 0
    extrasignal.status = 1 - status
    db.session.commit()
    msg = 'activated' if extrasignal.status is 1 else 'deactivated'
    flash('Extra signal {}, {} successfully.'.format(extrasignal.name, msg), 'success')
    return redirect(url_for('carboard.indexExtrasignal'))

# ------------------ /carboard/extrasignal/id/delete : Delete extrasignal --------------- #


@carboard.route('/extrasignal/<int:id>/delete', methods=['GET'])
@login_required
def deleteExtrasignal(id):
    extrasignal = Extrasignal.query.get_or_404(id)
    db.session.delete(extrasignal)
    db.session.commit()
    flash('Extra signal {}, deleted successfully.'.format(extrasignal.name), 'success')
    return redirect(url_for('carboard.indexExtrasignal'))
