from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from wtforms.validators import DataRequired, Regexp, Length

from ..models.model import Model
from ..models.brand import Brand

# ------------------------ custom validation methods ------------------------ #


def model_exist(form, field):
    if Model.select().where(Model.name == field.data).exists():
        raise ValidationError('Model already exists !')

# ---------------------------- Model form classes ---------------------------- #


class ModelForm(FlaskForm):
    """ Model add/edit FlaskForm """
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=2, max=50),
            Regexp(
                r'^[a-zA-Z0-9 ]+$',
                message=("Model name is not correct !")
            ),
        ]
    )
    brand_id = SelectField(
        'Brand',
        coerce=int,
        validators=[
            DataRequired(),
        ]
    )
