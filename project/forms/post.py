from ipaddress import summarize_address_range

from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, TextAreaField, validators


class PostForm(FlaskForm):
    title = StringField("Title", [validators.DataRequired()])
    summary = TextAreaField("Summary", [validators.DataRequired()])
    content = TextAreaField("Content", [validators.DataRequired()])
    is_markdown = BooleanField("Markdown")
    is_published = BooleanField("Published")
    submit = SubmitField("Save")
