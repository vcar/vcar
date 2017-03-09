from flask_wtf import Form
from wtforms import StringField, DateField
from wtforms.validators import ValidationError, DataRequired, Optional, Regexp, Length
from ..models.article import Article

# ------------------------ custom validation methods ------------------------ #


def article_exist(form, field):
    if Article.select().where(Article.name == field.data).exists():
        raise ValidationError('Article already exists !')

# ---------------------------- Article form classes ------------------------- #


class ArticleForm(Form):
    """ Article add/edit Form """
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=3, max=255),
            Regexp(
                r'^[a-zA-Z_\- ]+$',
                message=("Article name is not correct !")
            ),
        ]
    )
    abstract = StringField(
        'Abstract',
        validators=[
            DataRequired(),
        ]
    )
    authors = StringField(
        'Authors',
    )
    keywords = StringField(
        'Keywords',
    )
    publication_date = DateField(
        'Date of publication',
        format='%d/%m/%Y',
        validators=[
            Optional(),
        ]
    )

    reference = StringField(
        'Reference',
    )
    link = StringField(
        'Link to article',
    )
