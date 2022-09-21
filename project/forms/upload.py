from flask_wtf import FlaskForm
from wtforms import FileField, MultipleFileField, SubmitField, validators


class UploadForm(FlaskForm):
    files = MultipleFileField("File(s) Upload", [validators.DataRequired()])
    submit = SubmitField("Upload")
