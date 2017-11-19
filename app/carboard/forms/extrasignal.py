from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Regexp, Length

from ..models.extrasignal import Extrasignal

# ------------------------ custom validation methods ------------------------ #


def extrasignal_exist(form, field):
    if Extrasignal.select().where(Extrasignal.name == field.data).exists():
        raise ValidationError('Extra signal already exists !')

# ---------------------------- User form classes ---------------------------- #


class ExtrasignalForm(FlaskForm):
    """ Extrasignal add/edit FlaskForm """
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            # extrasignal_exist()
        ]
    )
    signal_id = SelectField(
        'Main signal',
        coerce=int,
        validators=[
            DataRequired(),
        ]
    )
    storage = SelectField(
        'Data Storage (Optionel)',
        validators = [
            DataRequired(),
        ]
    )
