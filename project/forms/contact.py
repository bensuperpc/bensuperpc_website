from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, validators


class ContactForm(FlaskForm):
    email = StringField("Email", [validators.DataRequired(), validators.Email()])
    # name = StringField("Name", [validators.DataRequired()])
    message = TextAreaField("Message", [validators.DataRequired()])
    submit = SubmitField("Upload")
