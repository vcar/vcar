from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Regexp, Length

from ..models.signalclass import Signalclass
# ------------------------ custom validation methods ------------------------ #

def signalclass_exist(form, field):
    if Signalclass.select().where(Signalclass.name == field.data).exists():
        raise ValidationError('Attribute already exists !')

# ---------------------------- Driver form classes ---------------------------- #


class SignalclassForm(Form):
    """ Signalclass add/edit Form """
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            # signalclass_exist()
        ]
    )

    description = TextAreaField(
        'Description',
        validators=[
            Length(min=0,max=1000)
        ]
    )

