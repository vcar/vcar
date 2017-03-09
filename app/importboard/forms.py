from flask_wtf import Form
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Regexp, Length
from .constants import DRIVER_GENDER


# ------------------------ custom validation methods ------------------------ #


# ---------------------------- Brand form classes ---------------------------- #

class VehicleForm(Form):
    """ Vehicle add/edit Form """
    brand_id = SelectField(
        'Brand',
        coerce=int,
        validators=[
            DataRequired(),
        ]
    )
    model_id = SelectField(
        'Model',
        coerce=int,
    )
    image = FileField(
        'Picture', validators=[
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only plz :) ')
        ]
    )

class DriverForm(Form):
    """ Driver add/edit Form """
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