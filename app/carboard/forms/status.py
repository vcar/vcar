from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp, Length

from ..models.status import Status

# ----------------------------- Status form classes ---------------------------


class StatusForm(FlaskForm):
    """ Status add/edit FlaskForm """
    title = StringField(
        'Status title',
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            Regexp(
                r'^[a-zA-Z ]+$',
                message=("Status title is not correct !")
            ),
        ]
    )
    color = StringField('Class color')
