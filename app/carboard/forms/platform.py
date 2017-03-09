from flask_wtf import Form
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp, Length

from ..models.platform import Platform

# ------------------------ custom validation methods ------------------------ #


def platform_exist(form, field):
    if Platform.select().where(Platform.name == field.data).exists():
        raise ValidationError('Platform already exists !')

# ---------------------------- Platform form classes ---------------------------- #


class PlatformForm(Form):
    """ Platform add/edit Form """
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            Regexp(
                r'^[a-zA-Z_\- ]+$',
                message=("Platform name is not correct !")
            ),
        ]
    )
    description = StringField(
        'Description',
        validators=[
            DataRequired(),
        ]
    )
    website = StringField(
        'Website',
    )
    logo = FileField(
        'Logo', validators=[
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only plz :) ')
        ]
    )
