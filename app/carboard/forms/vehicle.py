from flask_wtf import Form
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SelectField
from wtforms.validators import Optional, DataRequired, Regexp, Length

from ..models.vehicle import Vehicle

# ------------------------ custom validation methods ------------------------ #


def vehicle_exist(form, field):
    if Vehicle.select().where(Vehicle.name == field.data).exists():
        raise ValidationError('Vehicle already exists !')

# ---------------------------- Vehicle form classes ---------------------------- #

class VehicleForm(Form):
    """ Vehicle add/edit Form """
    user_id = SelectField(
        'User',
        coerce=int,
        validators=[
            DataRequired(),
        ]
    )
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
    driver_id = SelectField(
        'Driver',
        coerce=int,
    )
    image = FileField(
        'Picture', validators=[
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only plz :) ')
        ]
    )

class VehicleStatusForm(Form):
    """ Edit vehicle status Form """
    status_id = SelectField(
        'Status',
        coerce=int,
        validators=[
            DataRequired(),
        ]
    )
