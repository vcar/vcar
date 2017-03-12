from flask_wtf import Form
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Regexp, Length

from ..models.signal import Signal
# ------------------------ custom validation methods ------------------------ #

def signal_exist(form, field):
    if Signal.select().where(Signal.name == field.data).exists():
        raise ValidationError('Attribute already exists !')

# ---------------------------- Driver form classes ---------------------------- #


class SignalForm(Form):
    """ Signal add/edit Form """
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            # signal_exist()
        ]
    )
    signalclass_id = SelectField(
        'Signal class',
        coerce=int,
        validators=[
            DataRequired(),
        ]
    )
    signalsource_id = SelectField(
        'Signal source',
        coerce=int,
        validators=[
            DataRequired(),
        ]
    )
