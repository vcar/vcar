from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import login_required

from . import carboard
from ..models.country import Country
from ..forms.country import CountryForm
from ..helpers import paginate
from ..constants import PER_PAGE
from ...extensions import db


# --------------------- /carboard/country/ : List of countries ------------------ #

@carboard.route('/country/')
@login_required
def indexCountry():
    countries = Country.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    return render_template('carboard/country/index.html',
                           countries=countries
                           )

# ----------------------- /carboard/country/id : Show country ------------------- #


@carboard.route('/country/<int:id>', methods=['GET'])
@login_required
def showCountry(id):
    country = Country.query.get_or_404(id)
    return render_template('carboard/country/show.html',
                           country=country
                           )

# ---------------------- /carboard/country/new : Add country -------------------- #


@carboard.route('/country/new', methods=['GET', 'POST'])
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
        return redirect(url_for('carboard.indexCountry'))

    return render_template('carboard/country/new.html', form=form)

# -------------------- /carboard/country/id/edit : Edit country ----------------- #


@carboard.route('/country/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editCountry(id):
    """ Edit existing country """
    country = Country.query.get_or_404(id)
    form = CountryForm(obj=country)
    if form.validate_on_submit():
        form.populate_obj(country)
        db.session.commit()
        flash('Country {}, updated successfully.'.format(form.title.data), 'success')
        return redirect(url_for('carboard.showCountry', id=id))

    return render_template('carboard/country/edit.html', form=form, id=id)

# ------------------ /carboard/country/id/delete : Delete country --------------- #


@carboard.route('/country/<int:id>/toggle', methods=['GET'])
@login_required
def toggleCountry(id):
    country = Country.query.get_or_404(id)
    # getattr(country, 'status', 0)
    status = country.status if country.status is not None else 0;
    country.status = 1 - status
    db.session.commit()
    msg = 'activated' if country.status is 1 else 'deactivated'
    flash('Country {}, {} successfully.'.format(country.title, msg), 'success')
    return redirect(url_for('carboard.indexCountry'))

# ------------------ /carboard/country/id/delete : Delete country --------------- #


@carboard.route('/country/<int:id>/delete', methods=['GET'])
@login_required
def deleteCountry(id):
    country = Country.query.get_or_404(id)
    db.session.delete(country)
    db.session.commit()
    flash('Country {}, deleted successfully.'.format(country.title), 'success')
    return redirect(url_for('carboard.indexCountry'))
