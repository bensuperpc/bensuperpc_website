from flask_wtf import FlaskForm
from wtforms import FileField, MultipleFileField, SubmitField, validators


class UploadMultipleForm(FlaskForm):
    files = MultipleFileField("File(s) Upload", [validators.DataRequired()])
    submit = SubmitField("Upload")


class UploadSimpleForm(FlaskForm):
    file = FileField("File Upload", [validators.DataRequired()])
    submit = SubmitField("Upload")
