from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Regexp, Length

from ..models.signalsource import Signalsource


# ------------------------ custom validation methods ------------------------ #

def signalsource_exist(form, field):
    pass


# ---------------------------- Signalsource form classes -------------------- #


class SignalsourceForm(FlaskForm):
    """ Signalsource add/edit FlaskForm """
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            # Signalsource_exist()
        ]
    )

    description = TextAreaField(
        'Description',
        validators=[
            Length(min=0, max=1000)
        ]
    )
