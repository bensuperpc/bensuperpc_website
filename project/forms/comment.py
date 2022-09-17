from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
    validators
)


class CommentForm(FlaskForm):
    content = TextAreaField("Content", [validators.DataRequired()])
    submit = SubmitField("Save")
