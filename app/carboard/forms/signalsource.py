from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp, Length

from ..models.signalsource import Signalsource

# ------------------------ custom validation methods ------------------------ #

def signalsource_exist(form, field):
    pass

# ---------------------------- Signalsource form classes -------------------- #


class SignalsourceForm(Form):
    """ Signalsource add/edit Form """
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            # Signalsource_exist()
        ]
    )
