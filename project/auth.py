import json
import os
from secrets import token_urlsafe

import requests
from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from flask.json import jsonify
from flask_login import current_user, login_required, login_user, logout_user
from loguru import logger
from werkzeug.security import check_password_hash, generate_password_hash

from .db import User, db
from .forms.login import LoginForm
from .forms.registration import RegistrationForm
from requests_oauthlib import OAuth2Session

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
    session['client_id'] = ""
    session['client_secret'] = ""
    session['redirect_uri'] = "https://127.0.0.1:5000/login/google/callback"

    session['authorization_base_url'] = "https://accounts.google.com/o/oauth2/v2/auth"
    session['token_url'] = "https://www.googleapis.com/oauth2/v4/token"
    session['refresh_url'] = session['token_url'] # True for Google but not all providers.
    session['scope'] = ["openid", "email", "profile"]


    google = OAuth2Session(
        session['client_id'], scope=session['scope'], redirect_uri=session['redirect_uri'])
    authorization_url, state = google.authorization_url(session['authorization_base_url'],
                                                        # offline for refresh token
                                                        # force to always make user click authorize
                                                        access_type="offline", prompt="select_account")

    logger.info(f"Authorization URL: {authorization_url}")
    logger.info(f"State: {state}")

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


@auth.route("/login/google/callback")
def callback():

    google = OAuth2Session(session['client_id'], redirect_uri=session['redirect_uri'],
                           state=session['oauth_state'])
    token = google.fetch_token(session['token_url'], client_secret=session['client_secret'],
                               authorization_response=request.url)

    # We use the session as a simple DB for this example.
    session['oauth_token'] = token

    google = OAuth2Session(session['client_id'], token=session['oauth_token'])

    r = google.get('https://www.googleapis.com/oauth2/v1/userinfo')
    r_decoded = r.content.decode('utf-8')
    user_info = json.loads(r_decoded)
    logger.info(f"User info: {user_info}")

    if user_info["verified_email"]:
        logger.success("User email verified by Google")

        unique_id = user_info["id"]
        logger.info(f"User unique id: {unique_id}")

        users_email = user_info["email"]
        logger.info(f"User email: {users_email}")

        picture = user_info["picture"]
        logger.info(f"User picture: {picture}")

        users_name = user_info["given_name"]
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
