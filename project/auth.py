import loguru as logger
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .forms.registration import RegistrationForm
from .models import User

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.profile"))
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash("Please check your password and try again.")
        return redirect(url_for("auth.login"))

    login_user(user, remember=remember)
    return redirect(url_for("main.profile"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        email = form.email.data
        name = form.username.data
        password = form.password.data
        confirm = form.confirm.data
        tos = form.accept_tos.data

        if email == "" or name == "" or password == "" or confirm == "" or tos == False:
            flash("Please fill out all fields.")
            return render_template("signup.html", form=form)

        email_db = User.query.filter_by(email=email).first()
        if email_db:
            flash("Email address already exists.")
            return render_template("signup.html", form=form)

        if password != confirm:
            flash("Passwords do not match.")
            return render_template("signup.html", form=form)

        new_user = User(
            email=email,
            name=name,
            password=generate_password_hash(password, method="sha512"),
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Thanks for registering")
        return redirect(url_for("auth.login"))
    return render_template("signup.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
