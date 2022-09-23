import json
import os
from secrets import token_urlsafe

import requests
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask.json import jsonify
from flask_login import current_user, login_required, login_user, logout_user
from loguru import logger
from werkzeug.security import check_password_hash, generate_password_hash

from .db import User, db
from .forms.login import LoginForm
from .forms.registration import RegistrationForm
from .oauth import oauth

auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/",
)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        password = form.password.data
        email = form.email.data

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"), form=form)
        login_user(user, remember=form.remember_me.data)

        user.connect += 1

        user.last_connect = db.func.current_timestamp()

        db.session.commit()

        logger.info(f"{user.name} logged in")
        flash("Welcome back !", "success")
        return redirect(url_for("main.index"))

    return render_template("login.html", form=form)


@auth.route("/login/google")
def login_google():
    redirect_uri = url_for("auth.callback_google", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@auth.route("/authorize/google")
def callback_google():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token, None)

    if ["email_verified"]:
        email = user["email"]
        name = user["name"]
        given_name = user["given_name"]
        family_name = user["family_name"]
        picture = user["picture"]
        locale = user["locale"]
        openid = user["sub"]

        user = User.query.filter_by(email=email).first()
        if not user:
            new_user = User(
                email=email,
                name=name,
                id_google=openid,
                picture_url=picture,
                password=generate_password_hash(token_urlsafe(64), method="sha512"),
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash("Thanks for registering", "success")
            return redirect(url_for("main.index"))
        else:
            login_user(user)
            flash("Welcome back !", "success")
            return redirect(url_for("main.index"))
    else:
        flash("Google login failed", "danger")
        return redirect(url_for("auth.login"))

    return redirect("/")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegistrationForm(request.form)

    if form.validate_on_submit():
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
            flash("Passwords do not match.", "danger")
            return render_template("signup.html", form=form)

        new_user = User(
            email=email,
            name=name,
            password=generate_password_hash(password, method="sha512"),
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Thanks for registering", "success")
        return redirect(url_for("auth.login"))
    return render_template("signup.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logger.debug(f"User {current_user.name} ({current_user.email}) logged out")
    logout_user()
    return redirect(url_for("main.index"))
