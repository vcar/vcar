from flask_wtf import Form
from wtforms import FormField, FieldList, StringField, SelectField
from wtforms.fields.html5 import URLField
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import ValidationError, Optional, DataRequired, Regexp, Length, url
from ..models.dataset import Dataset
from .article import ArticleForm

# ------------------------ custom validation methods ------------------------ #


def dataset_exist(form, field):
    if Dataset.select().where(Dataset.name == field.data).exists():
        raise ValidationError('Dataset already exists !')

# ---------------------------- Dataset form classes ------------------------- #


class DatasetForm(Form):
    """ Dataset add/edit Form """
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            Regexp(
                r'^[a-zA-Z_\- ]+$',
                message=("Dataset name is not correct !")
            ),
        ]
    )
    slug = StringField(
        'Slug',
        validators=[
            Optional(),
            Length(min=3, max=50),
            Regexp(
                r'^[a-z_]+$',
                message=("Dataset slug is not correct !")
            ),
        ]
    )
    description = StringField(
        'Description',
        validators=[
            DataRequired(),
        ]
    )
    author = StringField(
        'Author',
    )
    lab = StringField(
        'Lab',
    )
    website = StringField(
        'Website',
    )


class FeedDatasetForm(Form):
    """ Dataset add/edit Form """

    where = SelectField(
        'Where is your dataset files?',
        coerce=int,
        choices=[
            (0, 'Pick a choice ...'),
            (1, 'In my local machine'),
            (2, 'On a remote server'),
            (3, 'In vCar platform server')
        ],
        validators=[DataRequired()]
    )

    # local_type = SelectField(
    #     'What is your data?',
    #     coerce=int,
    #     choices=[
    #         (0, 'Pick a choice ...'),
    #         (1, 'One file'),
    #         (2, 'One zip file'),
    #         (3, 'Multiple files')
    #     ],
    #     validators=[DataRequired()]
    # )
    # local_file = FileField(
    #     'Now select your file', validators=[
    #         FileAllowed(['json', 'csv', 'txt'], 'File format not supported !')
    #     ]
    # )
    # local_zip = FileField(
    #     'Now select your zip file', validators=[
    #         FileAllowed(['zip'], 'only zip files are supported !')
    #     ]
    # )

    remote = URLField(
        'Specify file link',
        validators=[
            Optional(),
            url(message='Sorry, this is not a valid URL,')
        ],
        # default='http://example.com/file.json'
    )

    vcar = StringField(
        'Path',
        validators=[Optional()],
        # default='http://example.com/file.json'
    )

    """
        ---------------------------------------------------
        Dependences :
            from wtforms import FormField, FieldList
        ---------------------------------------------------
        Nested Form :
            article = FormField(ArticleForm)
            article = FieldList(FormField(ArticleForm))
        ---------------------------------------------------
        Jinja implementation :
            {{ form.hidden_tag() }}
            {{ render_field(form.name) }}
            {{ render_field(form.description) }}
            {{ render_field(form.author) }}
            ...

            {% for subform in form.article %}
                {{ render_field(subform) }}
            {% endfor %}
        ---------------------------------------------------
    """
