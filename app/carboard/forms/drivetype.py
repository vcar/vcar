from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp, Length

from ..models.drivetype import DriveType

# ----------------------------- DriveType form classes ---------------------------


class DriveTypeForm(FlaskForm):
    """ Driver type add/edit FlaskForm """
    name = StringField(
        'Driver type name',
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            Regexp(
                r'^[a-zA-Z ]+$',
                message=("Driver type name is not correct !")
            ),
        ]
    )
