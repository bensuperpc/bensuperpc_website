#!/usr/bin/env python

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
    url_prefix="/",
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

    return render_template("auth/login.html", form=form)


@auth.route("/login/google")
def login_google():
    redirect_uri = url_for("auth.callback_google", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@auth.route("/authorize/google")
def callback_google():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token, None)

    if user.get("email_verified"):
        email = user.get("email")
        username = user.get("name")
        given_name = user.get("given_name")
        family_name = user.get("family_name")
        picture = user.get("picture")
        # locale = user["locale"]
        openid = user.get("sub")

        user = User.query.filter_by(email=email).first()
        if not user:
            new_user = User(
                email=email,
                username=username,
                name=given_name,
                last_name=family_name,
                id_google=openid,
                picture_url=picture,
                password=generate_password_hash(token_urlsafe(64), method="sha512"),
            )

            new_user.connect = 1
            new_user.last_connect = db.func.current_timestamp()

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash("Thanks for registering", "success")
            return redirect(url_for("main.index"))
        else:
            if not user.id_google:
                user.id_google = openid

            user.connect = 1
            user.last_connect = db.func.current_timestamp()
            db.session.commit()

            login_user(user)
            flash("Welcome back !", "success")
            return redirect(url_for("main.index"))
    else:
        flash("Google login failed", "danger")
        return redirect(url_for("auth.login"))
    return redirect("/")


# From https://docs.authlib.org/en/latest/client/frameworks.html
@auth.route("/login/github")
def login_github():
    redirect_uri = url_for("auth.callback_github", _external=True)
    return oauth.github.authorize_redirect(redirect_uri)


@auth.route("/authorize/github")
def callback_github():
    token = oauth.github.authorize_access_token()
    resp = oauth.github.get("user", token=token)
    resp.raise_for_status()
    user_info = resp.json()

    email = user_info["email"]
    username = user_info["name"]
    picture = user_info["avatar_url"]
    openid = user_info["id"]  # github id isn't openid compliant

    user = User.query.filter_by(email=email).first()
    if not user:
        new_user = User(
            email=email,
            username=username,
            name=username,
            last_name=username,
            id_github=openid,
            picture_url=picture,
            password=generate_password_hash(token_urlsafe(64), method="sha512"),
        )

        new_user.connect = 1
        new_user.last_connect = db.func.current_timestamp()

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash("Thanks for registering", "success")
        return redirect(url_for("main.index"))
    else:
        if not user.id_github:
            user.id_github = openid

        user.connect = 1
        user.last_connect = db.func.current_timestamp()
        db.session.commit()

        login_user(user)
        flash("Welcome back !", "success")
        return redirect(url_for("main.index"))
    return redirect("/")


@auth.route("/login/twitter")
def login_twitter():
    flash("Twitter login is not implemented yet", "danger")
    return redirect("/")


@auth.route("/authorize/twitter")
def callback_twitter():
    flash("Twitter login is not implemented yet", "danger")
    return redirect("/")


@auth.route("/login/facebook")
def login_facebook():
    flash("Facebook login is not implemented yet", "danger")
    return redirect("/")


@auth.route("/authorize/facebook")
def callback_facebook():
    flash("Facebook login is not implemented yet", "danger")
    return redirect("/")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegistrationForm(request.form)

    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        name = form.name.data
        last_name = form.last_name.data
        password = form.password.data
        confirm = form.confirm.data
        tos = form.accept_tos.data

        if (
            email == ""
            or username == ""
            or password == ""
            or confirm == ""
            or tos == False
        ):
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
            username=username,
            name=name,
            last_name=last_name,
            password=generate_password_hash(password, method="sha512"),
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Thanks for registering", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/signup.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logger.debug(f"User {current_user.name} ({current_user.email}) logged out")
    logout_user()
    return redirect(url_for("main.index"))
