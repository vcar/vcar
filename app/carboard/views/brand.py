from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import login_required

from . import carboard
from ..models.brand import Brand
from ..forms.brand import BrandForm
from ..helpers import paginate, upload_file
from ..constants import PER_PAGE, BRAND_LOGO_DIR
from ...extensions import db

# --------------------- /carboard/brand/ : List of brands ------------------ #

@carboard.route('/brand/')
@login_required
def indexBrand():
    brands = Brand.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    return render_template('carboard/brand/index.html', brands=brands)

# ----------------------- /carboard/brand/id : Show brand ------------------- #


@carboard.route('/brand/<int:id>', methods=['GET'])
@login_required
def showBrand(id):
    brand = Brand.query.get_or_404(id)
    return render_template('carboard/brand/show.html', brand=brand)

# ---------------------- /carboard/brand/new : Add brand -------------------- #


@carboard.route('/brand/new', methods=['GET', 'POST'])
@login_required
def newBrand():
    """ Add new brand """

    form = BrandForm()

    if form.validate_on_submit():
        logo = upload_file(form.logo.data, BRAND_LOGO_DIR)
        brand = Brand(
            name=form.name.data,
            code=form.code.data,
            logo=logo
        )
        db.session.add(brand)
        db.session.commit()
        flash('Brand {}, added successfully.'.format(form.name.data), 'success')
        return redirect(url_for('carboard.indexBrand'))

    return render_template('carboard/brand/new.html', form=form)

# -------------------- /carboard/brand/id/edit : Edit brand ----------------- #


@carboard.route('/brand/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editBrand(id):
    """ Edit existing brand """
    brand = Brand.query.get_or_404(id)
    oldLogo = brand.logo
    form = BrandForm(obj=brand)
    if form.validate_on_submit():
        form.populate_obj(brand)
        logo = upload_file(form.logo.data, BRAND_LOGO_DIR)
        if logo is None:
            brand.logo = oldLogo
        else:
            brand.logo = logo
        db.session.commit()
        flash('Brand {}, updated successfully.'.format(form.name.data), 'success')
        return redirect(url_for('carboard.showBrand', id=id))

    return render_template('carboard/brand/edit.html', form=form, id=id)

# ------------------ /carboard/brand/id/delete : Delete brand --------------- #


@carboard.route('/brand/<int:id>/toggle', methods=['GET'])
@login_required
def toggleBrand(id):
    brand = Brand.query.get_or_404(id)
    # getattr(brand, 'status', 0)
    status = brand.status if brand.status is not None else 0
    brand.status = 1 - status
    db.session.commit()
    msg = 'activated' if brand.status is 1 else 'deactivated'
    flash('Brand {}, {} successfully.'.format(brand.name, msg), 'success')
    return redirect(url_for('carboard.indexBrand'))

# ------------------ /carboard/brand/id/delete : Delete brand --------------- #


@carboard.route('/brand/<int:id>/delete', methods=['GET'])
@login_required
def deleteBrand(id):
    brand = Brand.query.get_or_404(id)
    db.session.delete(brand)
    db.session.commit()
    flash('Brand {}, deleted successfully.'.format(brand.name), 'success')
    return redirect(url_for('carboard.indexBrand'))
