import os

from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import login_required
from sqlalchemy import or_

from app.carboard.forms.filesignal import FileSignalForm
from . import carboard
from ..models.extrasignal import Extrasignal
from ..models.signal import Signal
from ..models.platform import Platform
from ..forms.extrasignal import ExtrasignalForm
from ..helpers import paginate, choices, remove_csv, find_id, CSVLoader, upload_csv, platform_choices
from ..constants import PER_PAGE, CSV_TEMP
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
    form.storage.choices = platform_choices('Select a Data Storage', 'name')

    if form.validate_on_submit():
        extrasignal = Extrasignal(
            name=form.name.data,
            signal_id=form.signal_id.data,
            storage=form.storage.data,
        )
        db.session.add(extrasignal)
        db.session.commit()
        flash('Extra signal {}, added successfully.'.format(form.name.data), 'success')
        return redirect(url_for('carboard.indexExtrasignal'))

    return render_template('carboard/extrasignal/new.html', form=form)

#------------------------- /carboard/extrasignal/bulk-add bulk add extra signals from file ------------------- #

@carboard.route('/extrasignal/bulk-add', methods=['GET', 'POST'])
@login_required
def bulkAddExtraSignal():
    """ Add new extrasignal """
    form = FileSignalForm()
    errors = None
    if form.validate_on_submit():
        f = upload_csv(form.file.data, CSV_TEMP)
        loader = CSVLoader(os.path.join(CSV_TEMP, form.file.data.filename))
        res = loader.load()
        try:
            for row in res:
                signal_id = find_id(Signal, row['Main Signal'])
                storage = row['Data Storage']
                if signal_id == -1:
                    if not errors: errors = []  # lazy instatiation
                    errors.append('The Extra Signal ' + row[
                        'Signal Name'] + ' could not be added  because of invalid Main Signal or Data Storage ')
                    continue
                extraSignal = Extrasignal(
                    name=row['Signal Name'],
                    signal_id=signal_id ,
                    storage=storage
                )
                db.session.add(extraSignal)
                db.session.commit()
        except KeyError:
            errors = ['Your file is Not well Formated, please review your file structure .']
        remove_csv(form.file.data.filename, CSV_TEMP)
        if not errors: flash('Signals Added Successfully !', 'success')
    return render_template('carboard/extrasignal/bulk.html', form=form, errors=errors)



# -------------------- /carboard/extrasignal/id/edit : Edit extrasignal ----------------- #


@carboard.route('/extrasignal/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editExtrasignal(id):
    """ Edit existing extrasignal """
    extrasignal = Extrasignal.query.get_or_404(id)
    form = ExtrasignalForm(obj=extrasignal)
    form.signal_id.choices = choices(Signal, 'Select main signal', 1)
    form.storage.choices = platform_choices('Select a Data Storage','name')

    if form.validate_on_submit():
        form.populate_obj(extrasignal)
        print(form.data)
        db.session.commit()
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

# ------------------ /carboard/extrasignal/search : extra signal lookup (by description or name)  --------------- #

@carboard.route('/extrasignal/search', methods=['GET'])
@login_required
def searchExtraSignal():
    param = request.args.get('table_search')
    extrasignals = Extrasignal.query.filter(Extrasignal.name.like('%' + param + '%')).paginate(
            page=request.args.get('page', 1, type=int),
            per_page=request.args.get('per_page', PER_PAGE, type=int),
        )
    return render_template('carboard/extrasignal/search.html', extrasignals=extrasignals)
