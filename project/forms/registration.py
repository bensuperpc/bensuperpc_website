from wtforms import BooleanField, Form, PasswordField, StringField, validators

class RegistrationForm(Form):
    username = StringField(
        "Username",
        [
            validators.Length(min=4, max=256),
            validators.DataRequired(),
            validators.Regexp(
                regex=r"^[a-zA-Z0-9_.-]+$",
                message="Password must contain only letters, numbers, underscores",
            ),
        ],
    )
    email = StringField(
        "Email Address", [validators.Length(min=6, max=128), validators.DataRequired()]
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
