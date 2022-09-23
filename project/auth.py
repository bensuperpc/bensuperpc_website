import json
import os
from secrets import token_urlsafe

import requests
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from loguru import logger
from werkzeug.security import check_password_hash, generate_password_hash

from .db import User, db
from .forms.login import LoginForm
from .forms.registration import RegistrationForm
from .google import google

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


@auth.route("/login/google", methods=["GET", "POST"])
def login_google():
    google_provider_cfg = google.get_google_provider_cfg()
    logger.info(google_provider_cfg)

    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    logger.info(authorization_endpoint)

    request_uri = google.client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@auth.route("/login/google/callback")
def callback():
    code = request.args.get("code")

    google_provider_cfg = google.get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = google.client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(google.GOOGLE_CLIENT_ID, google.GOOGLE_CLIENT_SECRET),
    )

    google.client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = google.client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        logger.success("User email verified by Google")

        unique_id = userinfo_response.json()["sub"]
        logger.info(f"User unique id: {unique_id}")

        users_email = userinfo_response.json()["email"]
        logger.info(f"User email: {users_email}")

        picture = userinfo_response.json()["picture"]
        logger.info(f"User picture: {picture}")

        users_name = userinfo_response.json()["given_name"]
        logger.info(f"User name: {users_name}")

        user = User.query.filter_by(email=users_email, id_google=unique_id).first()

        if not user:
            logger.info("User does not exist, creating a new user")
            new_user = User(
                email=users_email,
                name=users_name,
                id_google=unique_id,
                picture_url=picture,
                password=generate_password_hash(token_urlsafe(64), method="sha512"),
            )

            new_user.connect = 1
            new_user.last_connect = db.func.current_timestamp()

            db.session.add(new_user)
            db.session.commit()
            logger.info("User created")
            login_user(new_user, remember=True)
            flash("Thanks for registering !", "success")
            return redirect(url_for("main.index"))
        else:
            logger.info("User already exists, logging in")

            user.connect += 1
            user.last_connect = db.func.current_timestamp()
            db.session.commit()

            login_user(user, remember=True)
            flash("Welcome back !", "success")
            return redirect(url_for("main.index"))
    else:
        logger.warning("User email not available or not verified by Google.")


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
