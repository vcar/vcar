from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp, Length

from ..models.country import Country

# ------------------------ custom validation methods ------------------------ #


def country_exist(form, field):
    if Country.select().where(Country.title == field.data).exists():
        raise ValidationError('Country already exists !')

# ---------------------------- User form classes ---------------------------- #


class CountryForm(Form):
    """ Country add/edit Form """
    title = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            Regexp(
                r'^[a-zA-Z ]+$',
                message=("Country name is not correct !")
            ),
            # country_exist()
        ]
    )
    code = StringField(
        'Iso Code',
        validators=[
            DataRequired(),
            Length(min=2, max=2),
        ]
    )
