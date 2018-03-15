from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import login_required

from . import dashboard
from ..models.country import Country
from ..forms.country import CountryForm
from ..helpers.helpers import paginate
from ..constants.constants import PER_PAGE
from ...extensions import db


# --------------------- /dashboard/country/ : List of countries ------------------ #

@dashboard.route('/country/')
@login_required
def indexCountry():
    countries = Country.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    return render_template('dashboard/country/index.html',
                           countries=countries
                           )

# ----------------------- /dashboard/country/id : Show country ------------------- #


@dashboard.route('/country/<int:id>', methods=['GET'])
@login_required
def showCountry(id):
    country = Country.query.get_or_404(id)
    return render_template('dashboard/country/show.html',
                           country=country
                           )

# ---------------------- /dashboard/country/new : Add country -------------------- #


@dashboard.route('/country/new', methods=['GET', 'POST'])
@login_required
def newCountry():
    """ Add new country """

    form = CountryForm()

    if form.validate_on_submit():
        country = Country(
            title=form.title.data,
            code=form.code.data
        )
        db.session.add(country)
        db.session.commit()
        flash('Country {}, added successfully.'.format(form.title.data), 'success')
        return redirect(url_for('dashboard.indexCountry'))

    return render_template('dashboard/country/new.html', form=form)

# -------------------- /dashboard/country/id/edit : Edit country ----------------- #


@dashboard.route('/country/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editCountry(id):
    """ Edit existing country """
    country = Country.query.get_or_404(id)
    form = CountryForm(obj=country)
    if form.validate_on_submit():
        form.populate_obj(country)
        db.session.commit()
        flash('Country {}, updated successfully.'.format(form.title.data), 'success')
        return redirect(url_for('dashboard.showCountry', id=id))

    return render_template('dashboard/country/edit.html', form=form, id=id)

# ------------------ /dashboard/country/id/delete : Delete country --------------- #


@dashboard.route('/country/<int:id>/toggle', methods=['GET'])
@login_required
def toggleCountry(id):
    country = Country.query.get_or_404(id)
    # getattr(country, 'status', 0)
    status = country.status if country.status is not None else 0;
    country.status = 1 - status
    db.session.commit()
    msg = 'activated' if country.status is 1 else 'deactivated'
    flash('Country {}, {} successfully.'.format(country.title, msg), 'success')
    return redirect(url_for('dashboard.indexCountry'))

# ------------------ /dashboard/country/id/delete : Delete country --------------- #


@dashboard.route('/country/<int:id>/delete', methods=['GET'])
@login_required
def deleteCountry(id):
    country = Country.query.get_or_404(id)
    db.session.delete(country)
    db.session.commit()
    flash('Country {}, deleted successfully.'.format(country.title), 'success')
    return redirect(url_for('dashboard.indexCountry'))
