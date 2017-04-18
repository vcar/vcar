from flask_wtf import Form
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Optional, Length


# ------------------------ custom validation methods ------------------------ #


# ---------------------------- Chart form class ----------------------------- #

class ChartForm(Form):
    """ Chart add/edit Form """

    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=3, max=50),
        ]
    )
    driver_id = SelectField(
        'Driver',
        coerce=int,  # str
        validators=[
            Optional(),
        ]
    )
    vehicle_id = SelectField(
        'Driver',
        coerce=int,  # str
        validators=[
            Optional(),
        ]
    )
