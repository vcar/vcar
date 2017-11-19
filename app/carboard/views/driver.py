from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import login_required

from . import carboard
from ..models.driver import Driver
from ..models.user import User
from ..models.country import Country
from ..models.status import Status
from ..forms.driver import DriverForm
from ..helpers import paginate, choices, upload_file
from ..constants import PER_PAGE, DRIVER_LOGO_DIR
from ...extensions import db

# --------------------- /carboard/driver/ : List of drivers ------------------ #

@carboard.route('/driver/')
@login_required
def indexDriver():
    drivers = Driver.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    return render_template('carboard/driver/index.html', drivers=drivers)

# ----------------------- /carboard/driver/id : Show driver ------------------- #


@carboard.route('/driver/<int:id>', methods=['GET'])
@login_required
def showDriver(id):
    driver = Driver.query.get_or_404(id)
    return render_template('carboard/driver/show.html', driver=driver)

# ---------------------- /carboard/driver/new : Add driver -------------------- #


@carboard.route('/driver/new', methods=['GET', 'POST'])
@login_required
def newDriver():
    """ Add new driver """

    form = DriverForm()
    form.user_id.choices = choices(User, 'Select a user', 1, 'username')
    form.country_id.choices = choices(Country, 'Select a country', 1, 'title')
    form.status_id.choices = choices(Status, 'Select a status', False, 'title')

    if form.validate_on_submit():
        avatar = upload_file(form.avatar.data, DRIVER_LOGO_DIR)
        driver = Driver(
            gender=form.gender.data,
            fullname=form.fullname.data,
            user_id=form.user_id.data,
            status_id=form.status_id.data,
            country_id=form.country_id.data,
            city=form.city.data,
            avatar=avatar
        )
        db.session.add(driver)
        db.session.commit()
        flash('Driver {}, added successfully.'.format(form.fullname.data), 'success')
        return redirect(url_for('carboard.indexDriver'))

    return render_template('carboard/driver/new.html', form=form)

# -------------------- /carboard/driver/id/edit : Edit driver ----------------- #


@carboard.route('/driver/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editDriver(id):
    """ Edit existing driver """
    driver = Driver.query.get_or_404(id)
    oldAvatar = driver.avatar

    form = DriverForm(obj=driver)
    form.user_id.choices = choices(User, 'Select a user', 1, 'username')
    form.country_id.choices = choices(Country, 'Select a country', 1, 'title')
    form.status_id.choices = choices(Status, 'Select a status', False, 'title')

    if form.validate_on_submit():
        form.populate_obj(driver)
        avatar = upload_file(form.avatar.data, DRIVER_LOGO_DIR)
        if avatar is None:
            driver.avatar = oldAvatar
        else:
            driver.avatar = avatar
        db.session.commit()
        flash('Driver {}, updated successfully.'.format(form.fullname.data), 'success')
        return redirect(url_for('carboard.showDriver', id=id))

    return render_template('carboard/driver/edit.html', form=form, id=id)

# ------------------ /carboard/driver/id/delete : Delete driver --------------- #


@carboard.route('/driver/<int:id>/toggle', methods=['GET'])
@login_required
def toggleDriver(id):
    driver = Driver.query.get_or_404(id)
    # getattr(driver, 'status', 0)
    status = driver.status if driver.status is not None else 0
    driver.status = 1 - status
    db.session.commit()
    msg = 'activated' if driver.status is 1 else 'deactivated'
    flash('Driver {}, {} successfully.'.format(driver.fullname, msg), 'success')
    return redirect(url_for('carboard.indexDriver'))

# ------------------ /carboard/driver/id/delete : Delete driver --------------- #


@carboard.route('/driver/<int:id>/delete', methods=['GET'])
@login_required
def deleteDriver(id):
    driver = Driver.query.get_or_404(id)
    db.session.delete(driver)
    db.session.commit()
    flash('Driver {}, deleted successfully.'.format(driver.fullname), 'success')
    return redirect(url_for('carboard.indexDriver'))
