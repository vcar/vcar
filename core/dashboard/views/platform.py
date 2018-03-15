from flask import (
    render_template, request, flash, redirect, url_for, jsonify
)
from flask_login import login_required

from . import dashboard
from ..models.platform import Platform, PlatformSchema
from ..models.extrasignal import ExtrasignalSchema
from ..forms.platform import PlatformForm
from ..helpers.helpers import paginate, upload_file
from ..constants.constants import PER_PAGE, PLATFORM_LOGO_DIR
from ...extensions import db

# --------------------- /dashboard/platform/ : List of platforms ------------------ #


@dashboard.route('/platform/')
@login_required
def indexPlatform():
    platforms = Platform.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    return render_template('dashboard/platform/index.html', platforms=platforms)

# ----------------------- /dashboard/platform/id : Show platform ------------------- #


@dashboard.route('/platform/<int:id>', methods=['GET'])
@login_required
def showPlatform(id):
    platform = Platform.query.get_or_404(id)
    return render_template('dashboard/platform/show.html', platform=platform)

# ----------------------- /dashboard/platform/id/json : Json platform object ------- #


@dashboard.route('/platform/<int:id>/json', methods=['GET'])
@login_required
def jsonPlatform(id):
    platform = Platform.query.get_or_404(id)
    platform_schema = PlatformSchema()
    extrasignal_eschema = ExtrasignalSchema(many=True)
    platform_result = platform_schema.dump(platform)
    extrasignal_result = extrasignal_eschema.dump(platform.signals)

    return jsonify({
        'platform': platform_result.data,
        'signals': extrasignal_result.data
    })

# ---------------------- /dashboard/platform/new : Add platform -------------------- #


@dashboard.route('/platform/new', methods=['GET', 'POST'])
@login_required
def newPlatform():
    """ Add new platform """

    form = PlatformForm()

    if form.validate_on_submit():
        logo = upload_file(form.logo.data, PLATFORM_LOGO_DIR)
        platform = Platform(
            name=form.name.data,
            mimetype=form.mimetype.data,
            website=form.website.data,
            description=form.description.data,
            logo=logo
        )
        db.session.add(platform)
        db.session.commit()
        flash('Platform {}, added successfully.'.format(form.name.data), 'success')
        return redirect(url_for('dashboard.indexPlatform'))

    return render_template('dashboard/platform/new.html', form=form)

# -------------------- /dashboard/platform/id/edit : Edit platform ----------------- #


@dashboard.route('/platform/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editPlatform(id):
    """ Edit existing platform """
    platform = Platform.query.get_or_404(id)
    oldLogo = platform.logo
    form = PlatformForm(obj=platform)
    if form.validate_on_submit():
        form.populate_obj(platform)
        logo = upload_file(form.logo.data, PLATFORM_LOGO_DIR)
        if logo is None:
            platform.logo = oldLogo
        else:
            platform.logo = logo
        db.session.commit()
        flash('Platform {}, updated successfully.'.format(form.name.data), 'success')
        return redirect(url_for('dashboard.showPlatform', id=id))

    return render_template('dashboard/platform/edit.html', form=form, id=id)

# ------------------ /dashboard/platform/id/delete : Delete platform --------------- #


@dashboard.route('/platform/<int:id>/toggle', methods=['GET'])
@login_required
def togglePlatform(id):
    platform = Platform.query.get_or_404(id)
    # getattr(platform, 'status', 0)
    status = platform.status if platform.status is not None else 0
    platform.status = 1 - status
    db.session.commit()
    msg = 'activated' if platform.status is 1 else 'deactivated'
    flash('Platform {}, {} successfully.'.format(platform.name, msg), 'success')
    return redirect(url_for('dashboard.indexPlatform'))

# ------------------ /dashboard/platform/id/delete : Delete platform --------------- #


@dashboard.route('/platform/<int:id>/delete', methods=['GET'])
@login_required
def deletePlatform(id):
    platform = Platform.query.get_or_404(id)
    db.session.delete(platform)
    db.session.commit()
    flash('Platform {}, deleted successfully.'.format(platform.name), 'success')
    return redirect(url_for('dashboard.indexPlatform'))
