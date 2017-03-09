from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import login_required

from . import carboard
from ..models.platform import Platform
from ..forms.platform import PlatformForm
from ..helpers import paginate, upload_file
from ..constants import PER_PAGE, PLATFORM_LOGO_DIR
from ...extensions import db

# --------------------- /carboard/platform/ : List of platforms ------------------ #

@carboard.route('/platform/')
@login_required
def indexPlatform():
    platforms = Platform.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    return render_template('carboard/platform/index.html', platforms=platforms)

# ----------------------- /carboard/platform/id : Show platform ------------------- #


@carboard.route('/platform/<int:id>', methods=['GET'])
@login_required
def showPlatform(id):
    platform = Platform.query.get_or_404(id)
    return render_template('carboard/platform/show.html', platform=platform)

# ---------------------- /carboard/platform/new : Add platform -------------------- #


@carboard.route('/platform/new', methods=['GET', 'POST'])
@login_required
def newPlatform():
    """ Add new platform """

    form = PlatformForm()

    if form.validate_on_submit():
        logo = upload_file(form.logo.data, PLATFORM_LOGO_DIR)
        platform = Platform(
            name=form.name.data,
            website=form.website.data,
            description=form.description.data,
            logo=logo
        )
        db.session.add(platform)
        db.session.commit()
        flash('Platform {}, added successfully.'.format(form.name.data), 'success')
        return redirect(url_for('carboard.indexPlatform'))

    return render_template('carboard/platform/new.html', form=form)

# -------------------- /carboard/platform/id/edit : Edit platform ----------------- #


@carboard.route('/platform/<int:id>/edit', methods=['GET', 'POST'])
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
        return redirect(url_for('carboard.showPlatform', id=id))

    return render_template('carboard/platform/edit.html', form=form, id=id)

# ------------------ /carboard/platform/id/delete : Delete platform --------------- #


@carboard.route('/platform/<int:id>/toggle', methods=['GET'])
@login_required
def togglePlatform(id):
    platform = Platform.query.get_or_404(id)
    # getattr(platform, 'status', 0)
    status = platform.status if platform.status is not None else 0
    platform.status = 1 - status
    db.session.commit()
    msg = 'activated' if platform.status is 1 else 'deactivated'
    flash('Platform {}, {} successfully.'.format(platform.name, msg), 'success')
    return redirect(url_for('carboard.indexPlatform'))

# ------------------ /carboard/platform/id/delete : Delete platform --------------- #


@carboard.route('/platform/<int:id>/delete', methods=['GET'])
@login_required
def deletePlatform(id):
    platform = Platform.query.get_or_404(id)
    db.session.delete(platform)
    db.session.commit()
    flash('Platform {}, deleted successfully.'.format(platform.name), 'success')
    return redirect(url_for('carboard.indexPlatform'))
