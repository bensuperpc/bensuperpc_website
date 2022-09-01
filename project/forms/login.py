from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, validators


class LoginForm(FlaskForm):
    email = StringField(
        "Email Address", [validators.DataRequired(), validators.Email()]
    )
    password = PasswordField(
        "New Password",
        [validators.DataRequired()],
    )
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("logging")
