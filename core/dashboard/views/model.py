from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import login_required

from . import dashboard
from ..models.model import Model
from ..models.brand import Brand
from ..forms.model import ModelForm
from ..helpers.helpers import paginate, choices
from ..constants.constants import PER_PAGE, BRAND_LOGO_DIR
from ...extensions import db

# --------------------- /dashboard/model/ : List of models ------------------ #


@dashboard.route('/model/')
@login_required
def indexModel():
    models = Model.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    return render_template('dashboard/model/index.html', models=models)

# ----------------------- /dashboard/model/id : Show model ------------------- #


@dashboard.route('/model/<int:id>', methods=['GET'])
@login_required
def showModel(id):
    model = Model.query.get_or_404(id)
    return render_template('dashboard/model/show.html', model=model)

# ---------------------- /dashboard/model/new : Add model -------------------- #


@dashboard.route('/model/new', methods=['GET', 'POST'])
@login_required
def newModel():
    """ Add new model """

    form = ModelForm()
    form.brand_id.choices = choices(Brand)

    if form.validate_on_submit():
        model = Model(
            name=form.name.data,
            brand_id=form.brand_id.data,
        )
        db.session.add(model)
        db.session.commit()
        flash('Model {}, added successfully.'.format(form.name.data), 'success')
        return redirect(url_for('dashboard.indexModel'))

    return render_template('dashboard/model/new.html', form=form)

# -------------------- /dashboard/model/id/edit : Edit model ----------------- #


@dashboard.route('/model/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editModel(id):
    """ Edit existing model """
    model = Model.query.get_or_404(id)
    form = ModelForm(obj=model)
    form.brand_id.choices = choices(Brand)

    if form.validate_on_submit():
        form.populate_obj(model)
        db.session.commit()
        flash('Model {}, updated successfully.'.format(form.name.data), 'success')
        return redirect(url_for('dashboard.showModel', id=id))

    return render_template('dashboard/model/edit.html', form=form, id=id)

# ------------------ /dashboard/model/id/delete : Delete model --------------- #


@dashboard.route('/model/<int:id>/toggle', methods=['GET'])
@login_required
def toggleModel(id):
    model = Model.query.get_or_404(id)
    status = model.status if model.status is not None else 0
    model.status = 1 - status
    db.session.commit()
    msg = 'activated' if model.status is 1 else 'deactivated'
    flash('Model {}, {} successfully.'.format(model.name, msg), 'success')
    return redirect(url_for('dashboard.indexModel'))

# ------------------ /dashboard/model/id/delete : Delete model --------------- #


@dashboard.route('/model/<int:id>/delete', methods=['GET'])
@login_required
def deleteModel(id):
    model = Model.query.get_or_404(id)
    db.session.delete(model)
    db.session.commit()
    flash('Model {}, deleted successfully.'.format(model.name), 'success')
    return redirect(url_for('dashboard.indexModel'))
