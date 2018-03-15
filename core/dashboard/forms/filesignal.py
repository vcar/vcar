from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired


class FileSignalForm(FlaskForm):
    file = FileField(validators=[FileAllowed(['csv'], 'only .csv files are supported now'), FileRequired()])
