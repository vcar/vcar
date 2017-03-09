from flask_wtf import Form
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SelectField, DateTimeField
from wtforms.validators import Optional, DataRequired, Regexp, Length

from ..models.record import Record

# ------------------------ custom validation methods ------------------------ #


def vehicle_exist(form, field):
    if Record.select().where(Record.name == field.data).exists():
        raise ValidationError('Record already exists !')

# ---------------------------- Record form classes ---------------------------- #

class RecordForm(Form):
    """ Record add/edit Form """
    trace = FileField(
        'Record trace file', validators=[
            DataRequired(),
            FileAllowed(['json', 'txt', 'xml', 'csv', 'xsl'], 'File extension not allowed')
        ]
    )
    name = StringField(
        'Name',
        validators=[
            Optional(),
            Length(min=3, max=50),
            Regexp(
                r'^[a-zA-Z ]+$',
                message=("Brand name is not correct !")
            ),
        ]
    )
    user_id = SelectField(
        'User',
        coerce=int,
        validators=[
            DataRequired(),
        ]
    )
    drivetype_id = SelectField(
        'Drive Type',
        coerce=int,
        validators=[
            Optional(),
        ]
    )
    driver_id = SelectField(
        'Driver',
        coerce=int, # str
        validators=[
            Optional(),
        ]
    )
    vehicle_id = SelectField(
        'Driver',
        coerce=int, # str
        validators=[
            Optional(),
        ]
    )
    start = DateTimeField(
        'Starting record at',
        validators=[
            Optional(),
        ]
    )
    end = DateTimeField(
        'End record at',
        validators=[
            Optional(),
        ]
    )
    description = StringField(
        'Description',
        validators=[
            Optional(),
            Length(min=3),
        ]
    )

class RecordStatusForm(Form):
    """ Edit vehicle status Form """
    status_id = SelectField(
        'Status',
        coerce=int,
        validators=[
            DataRequired(),
        ]
    )
