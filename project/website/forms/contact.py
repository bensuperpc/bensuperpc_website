from turtle import title

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, validators


class ContactForm(FlaskForm):
    email = StringField("Email", [validators.DataRequired(), validators.Email()])
    title = StringField("Title", [validators.DataRequired()])
    # name = StringField("Name", [validators.DataRequired()])
    message = TextAreaField("Message", [validators.DataRequired()])
    submit = SubmitField("Upload")
