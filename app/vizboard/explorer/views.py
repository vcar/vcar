from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import (
    login_required, current_user
)

from .models import Chart
from .forms import ChartForm
from .helpers import choices

from .. import vizboard

from ...carboard.models.vehicle import Vehicle
from ...carboard.models.driver import Driver
from ...extensions import db

# --------------------- /vizboard/explorer/ : List of charts ------------------- #


@vizboard.route('/chart', methods=['GET'])
@login_required
def indexChart():
    charts = Chart.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', 10, type=int),
    )
    return render_template('vizboard/explorer/index.html', charts=charts)

# ----------------------- /vizboard/explorer/id : Show chart ------------------- #


@vizboard.route('/chart/<int:id>', methods=['GET'])
@login_required
def showChart(id):
    chart = Chart.query.get_or_404(id)
    return render_template('vizboard/explorer/show.html', chart=chart)

# ---------------------- /vizboard/explorer/new : Add new chart ----------- #


@vizboard.route('/chart/new', methods=['GET', 'POST'])
@login_required
def newChart():
    """ Add new chart"""

    form = ChartForm()
    form.driver_id.choices = choices(Driver, 'Select a Driver', False, 'fullname')
    form.vehicle_id.choices = choices(Vehicle, 'Select a vehicle')

    if form.validate_on_submit():
        chart = Chart(
            name=form.name.data,
            user_id=current_user.id,
            driver_id=form.driver_id.data,
            vehicle_id=form.vehicle_id.data,
            isValid=False,
            error="Not initialized yet"
        )

        db.session.add(chart)
        db.session.commit()
        return redirect(url_for('carboard.explorerChart'))

    return render_template('vizboard/explorer/new.html', form=form)

# -------------------- /vizboard/explorer/id/edit : Edit chart ----------------- #


@vizboard.route('/chart/<int:id>/explorer', methods=['GET', 'POST'])
@login_required
def explorerChart():
    """Setup chart via explorer """

    chart = Chart.query.get_or_404(id)

    # if form.validate_on_submit():
    #     trace = upload_file(form.trace.data, DRIVE_FILES_DIR)
    #     chart = Chart(
    #         user_id=form.user_id.data,
    #         driver_id=form.driver_id.data,
    #         vehicle_id=form.vehicle_id.data,
    #         name=form.name.data,
    #     )
    #     db.session.add(chart)
    #     db.session.commit()
    #     return redirect(url_for('carboard.explorerChart'))

    return render_template('vizboard/explorer/new.html', chart=chart)

# ------------------ /vizboard/explorer/id/delete : Delete chart --------------- #


@vizboard.route('/chart/<int:id>/toggle', methods=['GET', 'POST'])
@login_required
def toggleChart(id):
    chart = Chart.query.get_or_404(id)
    status = chart.status if chart.status is not None else 0
    chart.status = 1 - status
    db.session.commit()
    msg = 'activated' if chart.status is 1 else 'deactivated'
    flash('Chart {}, {} successfully.'.format(chart.name, msg), 'info')
    return redirect(url_for('carboard.indexChart'))

# ------------------ /vizboard/explorer/id/delete : Delete chart --------------- #


@vizboard.route('/chart/<int:id>/delete', methods=['GET'])
@login_required
def deleteChart(id):
    chart = Chart.query.get_or_404(id)
    db.session.delete(chart)
    db.session.commit()
    flash('Chart {}, deleted successfully.'.format(chart.name), 'info')
    return redirect(url_for('carboard.indexChart'))
