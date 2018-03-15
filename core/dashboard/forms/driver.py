from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Regexp, Length

from ..models.driver import Driver
from ..constants.constants import DRIVER_GENDER

# ------------------------ custom validation methods ------------------------ #


def driver_exist(form, field):
    if Driver.select().where(Driver.name == field.data).exists():
        raise ValidationError('Driver already exists !')

# ---------------------------- Driver form classes ---------------------------- #


class DriverForm(FlaskForm):
    """ Driver add/edit FlaskForm """
    gender = SelectField(
        'Gender',
        coerce=int,
        choices=DRIVER_GENDER,
        validators=[
            DataRequired(),
        ]
    )
    fullname = StringField(
        'Fullname',
        validators=[
            Length(min=3, max=50),
            Regexp(
                r'^[a-zA-Z ]+$',
                message=("Driver name is not correct !")
            ),
        ]
    )
    user_id = SelectField(
        'User',
        coerce=int,
        validators=[
            DataRequired(),
        ]
    )
    country_id = SelectField(
        'Country',
        coerce=int,
        validators=[
            DataRequired(),
        ]
    )
    status_id = SelectField(
        'Status',
        coerce=int,
        validators=[
            DataRequired(),
        ]
    )
    city = StringField(
        'City',
        validators=[
            Length(min=2, max=50),
        ]
    )
    avatar = FileField(
        'Avatar', validators=[
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only plz :) ')
        ]
    )
