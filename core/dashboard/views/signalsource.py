import os

from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import login_required
from sqlalchemy import or_

from . import dashboard
from ..models.signalsource import Signalsource
from ..forms.signalsource import SignalsourceForm
from ..forms.filesignal import FileSignalForm
from ..constants.constants import PER_PAGE, CSV_TEMP
from ..helpers.helpers import paginate, CSVLoader, remove_csv, upload_csv
from ...extensions import db


# --------------------- /dashboard/signalsource/ : List of signalsources ----- #


@dashboard.route('/signalsource/')
@login_required
def indexSignalsource():
    signalsources = Signalsource.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    start = (request.args.get('page', 1, type=int) - 1) * PER_PAGE + 1
    return render_template('dashboard/signalsource/index.html', signalsources=signalsources, start=start)


# ----------------------- /dashboard/signalsource/id : Show signalsource ----- #


@dashboard.route('/signalsource/<int:id>', methods=['GET'])
@login_required
def showSignalsource(id):
    signalsource = Signalsource.query.get_or_404(id)
    return render_template('dashboard/signalsource/show.html', signalsource=signalsource)


# ---------------------- /dashboard/signalsource/new : Add signalsource -------------------- #

@dashboard.route('/signalsource/new', methods=['GET', 'POST'])
@login_required
def newSignalsource():
    """ Add new signalsource """
    form = SignalsourceForm()

    if form.validate_on_submit():
        ret = Signalsource.query.filter_by(name=form.name.data).first()
        if ret:
            flash('Signal source {}, already exists in the database.'.format(form.name.data), 'error')
            return redirect(url_for('dashboard.indexSignalsource'))
        signalsource = Signalsource(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(signalsource)
        db.session.commit()
        flash('Signal source {}, added successfully.'.format(form.name.data), 'success')
        return redirect(url_for('dashboard.indexSignalsource'))

    return render_template('dashboard/signalsource/new.html', form=form)


# -------------------------------- /dashboard/signalsource/bulk-add add all from file -------------#

@dashboard.route('/signalsource/bulk-add', methods=['GET', 'POST'])
@login_required
def bulkAddSource():
    form = FileSignalForm()
    errors = None
    if form.validate_on_submit():
        try:
            f = upload_csv(form.file.data, CSV_TEMP)
            loader = CSVLoader(os.path.join(CSV_TEMP, form.file.data.filename))
            res = loader.load()
            already_there = False
            for row in res:
                ret = Signalsource.query.filter_by(name=row['Signal Source'])
                if ret:
                    already_there = True  # check to not add already added signal sources
                    continue
                signal_source = Signalsource(
                    name=row['Signal Source'],
                    description=row['Description']
                )
                db.session.add(signal_source)
                db.session.commit()
            remove_csv(form.file.data.filename, CSV_TEMP)
        except KeyError:
            errors = ['Your file is Not well Formated, please review your file structure .']
        if not errors and not already_there:
            flash('Signal sources added Succesfully', 'success')
        if already_there:
            flash('Some Signal sources are not added because they are already in the database', 'warning')
    return render_template('dashboard/signalsource/bulk.html', form=form, errors=errors)


# -------------------- /dashboard/signalsource/id/edit : Edit signalsource ----------------- #


@dashboard.route('/signalsource/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editSignalsource(id):
    """ Edit existing signalsource """
    signalsource = Signalsource.query.get_or_404(id)
    form = SignalsourceForm(obj=signalsource)
    if form.validate_on_submit():
        form.populate_obj(signalsource)
        db.session.commit()
        flash('Signal source {}, updated successfully.'.format(form.name.data), 'success')
        return redirect(url_for('dashboard.showSignalsource', id=id))

    return render_template('dashboard/signalsource/edit.html', form=form, id=id)


# ------------------ /dashboard/signalsource/id/delete : Delete signalsource --------------- #


@dashboard.route('/signalsource/<int:id>/toggle', methods=['GET'])
@login_required
def toggleSignalsource(id):
    signalsource = Signalsource.query.get_or_404(id)
    status = signalsource.status if signalsource.status is not None else 0
    signalsource.status = 1 - status
    db.session.commit()
    msg = 'activated' if signalsource.status is 1 else 'deactivated'
    flash('Signal source {}, {} successfully.'.format(signalsource.name, msg), 'success')
    return redirect(url_for('dashboard.indexSignalsource'))


# ------------------ /dashboard/signalsource/id/delete : Delete signalsource --------------- #


@dashboard.route('/signalsource/<int:id>/delete', methods=['GET'])
@login_required
def deleteSignalsource(id):
    signalsource = Signalsource.query.get_or_404(id)
    db.session.delete(signalsource)
    db.session.commit()
    flash('Signal source {}, deleted successfully.'.format(signalsource.name), 'success')
    return redirect(url_for('dashboard.indexSignalsource'))


# ------------------ /dashboard/signalsource/search?table_seach=? : Search for signal source --------------- #

@dashboard.route('/signalsource/search')
@login_required
def searchSignalSource():
    param = request.args.get('table_search')
    signalsources = Signalsource.query.filter(
        or_(Signalsource.name.like('%' + param + '%'), Signalsource.description.like('%' + param + '%'))).paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    return render_template('dashboard/signalsource/search.html', signalsources=signalsources)
