from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import login_required
import os

from sqlalchemy import or_

from . import dashboard
from ..models.signal import Signal
from ..models.signalclass import Signalclass
from ..models.signalsource import Signalsource
from ..forms.signal import SignalForm
from ..forms.filesignal import FileSignalForm
from ..helpers.helpers import paginate, choices, CSVLoader, find_id, types, get_signal_from_form, upload_csv, remove_csv
from ..constants.constants import PER_PAGE, CSV_TEMP
from ...extensions import db


# --------------------- /dashboard/signal/ : List of signals ----- #


@dashboard.route('/signal/')
@login_required
def indexSignal():
    signals = Signal.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    start = (request.args.get('page', 1, type=int) - 1) * PER_PAGE + 1 # get the pagination start number to render in the template
    return render_template('dashboard/signal/index.html', signals=signals, start=start)


# ----------------------- /dashboard/signal/id : Show signal ----- #


@dashboard.route('/signal/<int:id>', methods=['GET'])
@login_required
def showSignal(id):
    signal = Signal.query.get_or_404(id)
    return render_template('dashboard/signal/show.html', signal=signal)


# ---------------------- /dashboard/signal/new : Add signal -------------------- #


@dashboard.route('/signal/new', methods=['GET', 'POST'])
@login_required
def newSignal():
    """ Add new signal """
    form = SignalForm()
    form.signalclass_id.choices = choices(Signalclass, 'Select signal class', 1)
    form.signalsource_id.choices = choices(Signalsource, 'Select signal source', 1)
    form.type.choices = types()
    if form.validate_on_submit():
        signal = get_signal_from_form(form);
        db.session.add(signal)
        db.session.commit()
        flash('Signal {}, added successfully.'.format(form.name.data), 'success')
        return redirect(url_for('dashboard.indexSignal'))

    return render_template('dashboard/signal/new.html', form=form)


# ---------------------- /dashboard/signal/bulk-add : Add signals from file -------------------- #

@dashboard.route('/signal/bulk-add', methods=['GET', 'POST'])
@login_required
def bulkAdd():
    form = FileSignalForm()
    errors = None
    print(request.form.getlist('files'))
    if form.validate_on_submit():
        f = upload_csv(form.file.data, CSV_TEMP)
        loader = CSVLoader(os.path.join(CSV_TEMP, form.file.data.filename))
        res = loader.load()
        already_there = False
        try:
            for row in res:
                print(row)
                signal_class_id = find_id(Signalclass, row['Signal Class'])
                signal_source_id = find_id(Signalsource, row['Signal Source'])

                if signal_class_id == -1 or signal_source_id == -1:
                    if not errors: errors = []  # lazy instatiation
                    errors.append('The Signal ' + row[
                        'Signal Name'] + ' could not be added  because of invalid Signal Class or Signal Source ')
                    continue
                ret = Signal.query.filter_by(
                    name=row['Signal Name']).all()  # check if a signal with the same name already exists
                same = False
                for sig in ret:
                    if sig.signalsource_id == signal_source_id:
                        same = True
                        break
                if same:
                    already_there = True
                    continue
                signal = Signal(
                    name=row['Signal Name'],
                    signalclass_id=signal_class_id,
                    signalsource_id=signal_source_id,
                    frequency=row['Frequency'],
                    type=row['Type'],
                    description=row['Description'],
                    unit=row['Unit']
                )
                signal.range = row['Range']
                db.session.add(signal)
                db.session.commit()
        except KeyError:
            errors = ['Your file is Not well Formated, please review your file structure .']
        remove_csv(form.file.data.filename, CSV_TEMP)
        if not errors: flash('Signals Added Successfully !', 'success')
        if already_there:
            flash('Some Signals are not added because they are already in the database', 'warning')
    return render_template('dashboard/signal/bulk.html', form=form, errors=errors)


# -------------------- /dashboard/signal/id/edit : Edit signal ----------------- #


@dashboard.route('/signal/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editSignal(id):
    """ Edit existing signal """
    signal = Signal.query.get_or_404(id)
    form = SignalForm(obj=signal)
    print(form.data)
    form.signalclass_id.choices = choices(Signalclass, 'Select signal class', 1)
    form.signalsource_id.choices = choices(Signalsource, 'Select signal source', 1)
    form.type.choices = types()
    if form.validate_on_submit():
        form.populate_obj(signal)
        db.session.commit()
        flash('Signal {}, updated successfully.'.format(form.name.data), 'success')
        return redirect(url_for('dashboard.showSignal', id=id))

    return render_template('dashboard/signal/edit.html', form=form, id=id)


# ------------------ /dashboard/signal/id/delete : Delete signal --------------- #


@dashboard.route('/signal/<int:id>/toggle', methods=['GET'])
@login_required
def toggleSignal(id):
    signal = Signal.query.get_or_404(id)
    status = signal.status if signal.status is not None else 0
    signal.status = 1 - status
    db.session.commit()
    msg = 'activated' if signal.status is 1 else 'deactivated'
    flash('Signal {}, {} successfully.'.format(signal.name, msg), 'success')
    return redirect(url_for('dashboard.indexSignal'))


# ------------------ /dashboard/signal/id/delete : Delete signal --------------- #


@dashboard.route('/signal/<int:id>/delete', methods=['GET'])
@login_required
def deleteSignal(id):
    signal = Signal.query.get_or_404(id)
    db.session.delete(signal)
    db.session.commit()
    flash('Signal {}, deleted successfully.'.format(signal.name), 'success')
    return redirect(url_for('dashboard.indexSignal'))

# ------------------ /dashboard/signal/search : signal lookup (by description or name)  --------------- #

@dashboard.route('/signal/search', methods=['GET'])
@login_required
def searchSignal():
    param = request.args.get('table_search')
    signals = Signal.query.filter(
        or_(Signal.name.like('%' + param + '%'), Signal.description.like('%' + param + '%')))\
        .paginate(
            page=request.args.get('page', 1, type=int),
            per_page=request.args.get('per_page', PER_PAGE, type=int),
        )
    return render_template('dashboard/signal/search.html', signals=signals)
