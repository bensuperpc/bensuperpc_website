from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, validators


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        [
            validators.Length(min=4, max=256),
            validators.DataRequired(),
            validators.Regexp(
                "^[A-Za-z0-9_.]*$", message="Username must contain only letters, numbers, underscores and points"
            ),
        ],
    )

    name = StringField(
        "Name",
        [
            validators.Length(min=4, max=256),
            validators.DataRequired(),
        ],
    )

    last_name = StringField(
        "Last name",
        [
            validators.Length(min=4, max=256),
            validators.DataRequired(),
        ],
    )

    email = StringField(
        "Email Address", [validators.DataRequired(), validators.Email()]
    )
    password = PasswordField(
        "New Password",
        [
            validators.DataRequired(),
            validators.EqualTo("confirm"),
            validators.Length(min=6, max=128),
        ],
    )
    confirm = PasswordField("Repeat Password")
    accept_tos = BooleanField("I accept the TOS", [validators.DataRequired()])
    submit = SubmitField("Register")
