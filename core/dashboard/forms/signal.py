from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Regexp, Length, ValidationError

from ..models.signal import Signal


# ------------------------ custom validation methods ------------------------ #

def signal_exist(form, field):
    if Signal.select().where(Signal.name == field.data).exists():
        raise ValidationError('Attribute already exists !')


# ---------------------------- Driver form classes ---------------------------- #


class SignalForm(FlaskForm):
    """ Signal add/edit FlaskForm """
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            # signal_exist()
        ]
    )

    type = SelectField(
        'Type',
        validators=[
            DataRequired()
        ]
    )

    unit = StringField(
        'Unit'
    )

    min_value = StringField(
        'no_min_value'
    )
    max_value = StringField(
        'no_max_value'
    )

    number = StringField(
        'no-number'
    )

    values = StringField(
        'no-values'
    )
    frequency = StringField(
        'Frequency'
    )
    description = TextAreaField(
        'Description',
        validators=[
            Length(min=0, max=1000)
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
