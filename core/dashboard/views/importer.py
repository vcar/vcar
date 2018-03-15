import json
from os.path import basename
from importlib import import_module
from threading import Thread
from flask import (
    Blueprint, Response, render_template, request, session, flash, redirect, url_for
)
from flask_login import (
    login_user, logout_user, login_required, current_user
)

from . import dashboard
from ..models.platform import Platform
from ..models.vehicle import Vehicle
from ..models.driver import Driver
from ..models.brand import Brand
from ..models.model import Model
from ..models.country import Country
from ..models.status import Status
from ..models.file import File
from ..forms.importer import VehicleForm, DriverForm
from ..utils.transformer import Transformer
from ..utils.platforms.openxc.indexing import task_info
from ..helpers.importer import checkSteps, choices, upload_file, upload_trace
from ..constants.constants import VEHICLE_LOGO_DIR, DRIVER_LOGO_DIR
from ...extensions import db


# -------------------- /stream : Redis stream server ------------------------ #


@dashboard.route('/stream')
def stream():
    return Response(task_info(), mimetype="text/event-stream")

# -------------------- /dashboard/old-importer : Introduce import wizard -------------------------- #


@dashboard.route('/importer')
@login_required
def indexImporter():
    """ Index :: Choosing a template """
    return render_template('dashboard/importer/index.html')










# -------------------- /dashboard/old-importer : Introduce import wizard -------------------------- #


@dashboard.route('/old-importer')
@login_required
def indexOldImporter():
    """ Import index page, containe wellcome text """
    return render_template('dashboard/old-importer/index.html')

# -------------------- /dashboard/old-importer/platform : Choose platform -------------------------- #


@dashboard.route('/old-importer/platform', methods=['GET', 'POST'])
@login_required
def platformOldImporter():
    """Select upload files platform in order to process indexing correctly"""
    platforms = Platform.query.filter_by(status=1).all()
    if request.method == 'POST':
        wizard_platform = request.form.get('platform', False)
        if wizard_platform is not False:
            session['import'] = {}
            session['import']['user'] = current_user.id
            session['import']['platform'] = int(request.form['platform'])
            session.modified = True
            return redirect(url_for('importer.vehicle'))
        else:
            session['import'] = {}
            session.modified = True
            # session.clear();
    return render_template('dashboard/old-importer/platform.html', platforms=platforms)

# -------------------- /dashboard/old-importer/vehicle : Choose or add a vehicle ------------------- #


@dashboard.route('/old-importer/vehicle', methods=['GET', 'POST'])
@login_required
def vehicleOldImporter():
    """Select or Add the vehicle used to generate traces"""
    check = checkSteps(step=1)
    if check is True:
        # Preparing data
        vehicle_selected = False
        vehicles = Vehicle.query.filter_by(
            user_id=current_user.id, status_id=1).all()
        form = VehicleForm()
        form.brand_id.choices = choices(Brand, 'Select a brand')
        form.model_id.choices = choices(Model, 'Select a model')

        # Geting selected vehicle if any
        if request.method == 'POST':
            wizard_vehicle = request.form.get('vehicle', False)
            if wizard_vehicle is not False:
                session['import']['vehicle'] = int(request.form['vehicle'])
                session.modified = True
                vehicle_selected = True
                return redirect(url_for('importer.driver'))

        # Adding a new vehicle if any
        if vehicle_selected is False and form.validate_on_submit():
            image = upload_file(form.image.data, VEHICLE_LOGO_DIR)
            vehicle = Vehicle(
                user_id=current_user.id,
                brand_id=form.brand_id.data,
                model_id=form.model_id.data,
                image=image
            )
            db.session.add(vehicle)
            db.session.commit()
            session['import']['vehicle'] = vehicle.id
            session.modified = True
            flash('Vehicle {}, added successfully.'.format(vehicle), 'success')
            return redirect(url_for('importer.driver'))

        # Rendring view template
        return render_template(
            'importer/vehicle.html',
            vehicles=vehicles,
            form=form
        )
    else:
        return check


# -------------------- /dashboard/old-importer/driver : Choose or add a driver --------------------- #

@dashboard.route('/old-importer/driver', methods=['GET', 'POST'])
@login_required
def driverOldImporter():
    """Select or Add the driver"""
    check = checkSteps(step=2)
    if check is True:
        # preparing data
        driver_selected = False
        drivers = Driver.query.filter_by(
            user_id=current_user.id, status_id=1).all()
        form = DriverForm()
        form.country_id.choices = choices(
            Country, 'Select a country', 1, 'title')
        form.status_id.choices = choices(
            Status, 'Select a status', False, 'title')
        # geting selected vehicle if any
        if request.method == 'POST':
            wizard_driver = request.form.get('driver', False)
            if wizard_driver is not False:
                session['import']['driver'] = int(request.form['driver'])
                session.modified = True
                driver_selected = True
                return redirect(url_for('importer.records'))
        # # adding a new vehicle if any
        if driver_selected is False and form.validate_on_submit():
            avatar = upload_file(form.avatar.data, DRIVER_LOGO_DIR)
            driver = Driver(
                gender=form.gender.data,
                fullname=form.fullname.data,
                user_id=current_user.id,
                status_id=form.status_id.data,
                country_id=form.country_id.data,
                city=form.city.data,
                avatar=avatar
            )
            db.session.add(driver)
            db.session.commit()
            session['import']['driver'] = driver.id
            session.modified = True
            flash('Driver {}, added successfully.'.format(driver), 'success')
            return redirect(url_for('importer.records'))

        return render_template(
            'importer/driver.html',
            drivers=drivers,
            form=form
        )
    else:
        return check

# -------------------- /dashboard/old-importer/records : Uplaod and process record files ----------- #


@dashboard.route('/old-importer/records', methods=['GET', 'POST'])
@login_required
def recordsOldImporter():
    check = checkSteps(step=3)
    if check is True:
        if request.method == 'POST':
            files = request.form.getlist('files')
            if files:
                """
                    Process data indexing using the python module associated
                    with the selected platform.
                    Every platform folder should containe a module named: indexing.py
                """
                try:
                    # Get the platform slug a.k.a module name
                    slug = Platform.query.get_or_404(
                        session['import']['platform']).slug
                    # Import the module
                    mod = import_module(
                        ".indexing", 'app.importer.platforms.' + slug)
                    # Indexing function
                    index_function = 'index_bulk'  # 'index'
                    # get a reference to the init function
                    init = getattr(mod, index_function)
                    # create a threaded job to index uploaded data according to
                    # it's platform
                    thread = Thread(target=init, args=[files, session['import']])
                    # thread.daemon = True
                    thread.start()
                    # thread.join(1)
                    # print(active_count())
                    flash('Your records are being indexed in background.', 'info')
                    return redirect(url_for('carboard.index'))
                except:
                    raise
            else:
                session['import']['files'] = []
                session.modified = True
                flash('Please upload some files', 'success')
                return redirect(url_for('importer.records'))

        return render_template('dashboard/old-importer/records.html')
    else:
        return check

# -------------------- /dashboard/old-importer/records : Uplaod record files ----------------------- #


@dashboard.route('/old-importer/getfile', methods=['POST'])
@login_required
def getfileOldImporter():
    """ Import trace files"""
    if request.method == 'POST':
        uploaded_file = upload_trace('openxc', current_user.id)
        if uploaded_file['status'] is True:
            file = File(
                user_id=current_user.id,
                filename=basename(uploaded_file['message']),
                path=uploaded_file['message']
            )
            db.session.add(file)
            db.session.commit()

            if "files" in session['import']:
                files = session['import']['files']
            else:
                files = []
            files.append(uploaded_file['message'])
            session['import']['files'] = files
            session.modified = True
        return json.dumps(uploaded_file)

# -------------------- /dashboard/old-importer/process : index files using elasticsearch ----------- #


@dashboard.route('/old-importer/process', methods=['GET', 'POST'])
@login_required
def processOldImporter():
    """
        Process data indexing using the python module associated
        with the selected platform.
        Every platform folder should containe a module named: indexing.py
    """
    if request.method == 'POST':
        files = request.form.getlist('files')
        if files:
            try:
                # Get the platform slug a.k.a module name
                slug = Platform.query.get_or_404(
                    session['import']['platform']).slug
                # Import the module
                mod = import_module(
                    ".indexing", 'app.importer.platforms.' + slug)
                # Indexing function
                index_function = 'index_bulk'  # 'index'
                # get a reference to the init function
                init = getattr(mod, index_function)
                # create a threaded job to index uploaded data according to
                # it's platform

                thread = Thread(target=init, args=[files, session['import']])
                # thread.daemon = True
                thread.start()
                # thread.join(1)
                # print(active_count())
            except:
                raise
        else:
            session['import']['files'] = []
            session.modified = True
            flash('Please upload some files before getting here', 'success')
            return redirect(url_for('importer.records'))

        return render_template('dashboard/old-importer/porcess.html')

# -------------------- /dashboard/old-importer/help : Show user ------------------------ #


@dashboard.route('/old-importer/help', methods=['GET'])
def helpOldImporter():
    # endpoints = [rule.rule for rule in app.url_map.iter_rules()
    #            if rule.endpoint !='static']
    # return jsonify(dict(api_endpoints=endpoints))
    # return render_template('dashboard/import/openxc_porcess.html')
    tr = Transformer()
    tr.setPlatformById(1)
    a = 'Speeda'
    x = tr.getInfo(a, ignore=False)
    raise


def dispatcherOldImporter(data=None):
    pass
    # if data:
    #
    # else:
    #     return None
    #
    # if request.method == 'POST':
    #     files = request.form.getlist('files')
    #     if files:
    #         thread = Thread(target=openxc_task, args=[traces, current_user.id])
    #         thread.daemon = True
    #         thread.start()
    #         # thread.join(1)
    #         # print(active_count())
    #             raise
    #     else:
    #         session['import']['files'] = []
    #         flash('Please upload some files before getting here', 'success')
    #         return redirect(url_for('importer.records'))
