from flask_wtf import Form
from flask_wtf.file import FileAllowed, FileField


class FileSignalForm(Form):
    file = FileField(validators=[FileAllowed(['csv'], 'only .csv files are supported now')])
