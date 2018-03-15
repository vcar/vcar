from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp, Length

from ..models.brand import Brand

# ------------------------ custom validation methods ------------------------ #


def brand_exist(form, field):
    if Brand.select().where(Brand.name == field.data).exists():
        raise ValidationError('Brand already exists !')

# ---------------------------- Brand form classes ---------------------------- #


class BrandForm(FlaskForm):
    """ Brand add/edit FlaskForm """
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            Regexp(
                r'^[a-zA-Z ]+$',
                message=("Brand name is not correct !")
            ),
        ]
    )
    code = StringField(
        'Code',
        validators=[
            DataRequired(),
            Length(min=2, max=2),
        ]
    )
    logo = FileField(
        'Logo', validators=[
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only plz :) ')
        ]
    )
