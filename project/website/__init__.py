#!/usr/bin/env python

# Import Python libs
import json
import os
from datetime import timedelta

# Import Flask libs
from flask import Flask, redirect, request
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

import tweepy
from dotenv import load_dotenv
from github3 import GitHub
from loguru import logger
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy_utils import database_exists, create_database, drop_database

# Import all blueprint
from .admin import admin as admin_blueprint
from .article import article as article_blueprint
from .auth import auth as auth_blueprint
from .db import Comment, Mutual, Post, User, db
from .error import error as error_blueprint
from .letter import letter as letter_blueprint
from .main import main as main_blueprint
from .oauth import oauth
from .user import user as user_blueprint


def create_app(*args, **kwargs):

    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, ".env"))

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["WTF_CSRF_SECRET_KEY"] = os.environ.get("WTF_CSRF_SECRET_KEY")

    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB
    app.config["UPLOAD_FOLDER"] = "uploads"

    app.config["REMEMBER_COOKIE_SECURE"] = True
    app.config["REMEMBER_COOKIE_NAME"] = "remember_token"
    app.config["REMEMBER_COOKIE_DOMAIN"] = "bensuperpc.com"

    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

    POSTGRES_URL = os.environ.get("POSTGRES_URL")
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PW = os.environ.get("POSTGRES_PW")
    POSTGRES_DB = os.environ.get("POSTGRES_DB")
    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)

    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    logger.info("Database URL: {url}", url=DB_URL)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    logger.debug("App DB initialized")

    # CSRF protection
    csrf = CSRFProtect()
    csrf.init_app(app)
    logger.debug("App CSRF initialized")

    # Login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    # login_manager.refresh_view = "accounts.reauthenticate"
    # login_manager.anonymous_user = MyAnonymousUser
    login_manager.session_protection = "strong"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # @login_manager.unauthorized_handler
    # def unauthorized():
    #    return redirect("/login")

    app.register_blueprint(main_blueprint)

    app.register_blueprint(auth_blueprint)

    app.register_blueprint(user_blueprint)

    app.register_blueprint(article_blueprint)

    app.register_blueprint(admin_blueprint)

    app.register_blueprint(letter_blueprint)

    app.register_blueprint(error_blueprint)

    logger.debug(f"{app.name} is running on {app.config['ENV']}")

    GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID", None)
    GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET", None)

    if GITHUB_CLIENT_ID is None or GITHUB_CLIENT_SECRET is None:
        logger.error(
            "GITHUB_CLIENT_ID or GITHUB_CLIENT_SECRET is not set, you need to set it in .env file"
        )
        exit(1)

    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)

    if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
        logger.error(
            "GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET is not set, you need to set it in .env file"
        )
        exit(1)

    TWITTER_BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN", None)

    if TWITTER_BEARER_TOKEN is None:
        logger.error("TWITTER_BEARER_TOKEN is not set, you need to set it in .env file")
        exit(1)

    oauth.init_app(app)
    logger.info("OAuth initialized")
    oauth.register(
        name="google",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={
            "scope": "openid email profile",
            "prompt": "select_account",
        },
    )
    """
    oauth.register(
        name='google',
        client_id=os.environ.get("GOOGLE_CLIENT_ID", None),
        client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", None),
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        client_kwargs={'scope': 'openid email profile'},
    )
    """
    logger.info("Google OAuth registered")

    oauth.register(
        name="github",
        client_id=GITHUB_CLIENT_ID,
        client_secret=GITHUB_CLIENT_SECRET,
        access_token_url="https://github.com/login/oauth/access_token",
        access_token_params=None,
        authorize_url="https://github.com/login/oauth/authorize",
        authorize_params=None,
        api_base_url="https://api.github.com/",
        client_kwargs={"scope": "user:email"},
    )
    logger.info("Github OAuth registered")

    """
    oauth.register(
        name='facebook',
        client_id=os.environ.get("FACEBOOK_CLIENT_ID", None),
        client_secret=os.environ.get("FACEBOOK_CLIENT_SECRET", None),
        access_token_url='https://graph.facebook.com/v2.8/oauth/access_token',
        access_token_params=None,
        authorize_url='https://www.facebook.com/v2.8/dialog/oauth',
        authorize_params=None,
        api_base_url='https://graph.facebook.com/v2.8/',
        client_kwargs={'scope': 'email'},
    )
    """


    # Load all data into the database
    with app.app_context():
        #if database_exists(DB_URL):
        #    logger.info("Deleting database")
            # drop_database(DB_URL)
        if not database_exists(DB_URL):
            logger.info("Creating database")
            create_database(DB_URL)

        db.create_all()
        db.session.commit()

        gh = GitHub(GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET)

        # Add new articles for testing
        data = {}
        with open(
            os.path.join(basedir, "static/data/article.json"), encoding="UTF-8"
        ) as json_file:
            data = json.load(json_file)

        for item in data["articles"]:

            logger.debug(f"Adding article {item['title']}")
            content = None

            if item["from_github"] == True:
                try:
                    content = gh.repository(
                        item["user"], item["repository"]
                    ).file_contents(item["file"])
                except:
                    logger.error(
                        f"Cannot get content from {item['user']}/{item['repository']}/{item['file']}"
                    )
                    continue
                content = content.decoded.decode("utf-8")
            else:
                content = item["content"]
            post = Post(
                title=item["title"],
                content=content,
                summarize=item["description"],
                # picture_url=item["picture_url"],
                is_markdown=True,
            )

            if (
                bool(db.session.query(Post).filter_by(title=item["title"]).first())
                is False
            ):
                db.session.add(post)
                db.session.commit()
                logger.debug(f"{post.title} added")
            else:
                logger.debug(f"{item['title']} already exists")

        # Add new users only for testing
        logger.warning("Adding users, only for testing/dev !")
        data = {}
        with open(
            os.path.join(basedir, "static/data/user.json"), encoding="UTF-8"
        ) as json_file:
            data = json.load(json_file)

        for item in data["users"]:
            new_user = User(
                email=item["email"],
                name=item["name"],
                password=generate_password_hash(item["password"], method="sha512"),
                admin=item["admin"],
                picture_url=item["picture_url"],
            )

            if (
                bool(db.session.query(User).filter_by(email=item["email"]).first())
                is False
            ):
                db.session.add(new_user)
                db.session.commit()
                logger.info(f"{new_user.name} added")

        # Add mutuals for testing
        TwitterClient = tweepy.Client(TWITTER_BEARER_TOKEN)
        data = {}
        with open(
            os.path.join(basedir, "static/data/mutual.json"), encoding="UTF-8"
        ) as json_file:
            data = json.load(json_file)

        for item in data["mutuals"]:
            profile_image_url = None
            try:
                twitter_name = item["twitter_url"].split("/")[-1]
                response = TwitterClient.get_users(
                    usernames=[twitter_name], user_fields=["profile_image_url"]
                )
                profile_image_url = response.data[0]["profile_image_url"]

                # Replace _normal with _400x400
                profile_image_url = profile_image_url.replace("_normal", "_400x400")
            except:
                profile_image_url = ""

            mutual = Mutual(
                name=item["name"],
                describe=item["describe"],
                picture_url=profile_image_url,
                website_url=item["website_url"],
                twitter_url=item["twitter_url"],
                discord_url=item["discord_url"],
                youtube_url=item["youtube_url"],
                github_url=item["github_url"],
            )

            if (
                bool(db.session.query(Mutual).filter_by(name=item["name"]).first())
                is False
            ):
                db.session.add(mutual)
                db.session.commit()
                logger.info("Added mutual {}".format(mutual.name))
            else:
                logger.info("Mutual {} already exists".format(item["name"]))

        # Add comments for testing
        # logger.warning("Adding comments only for testing")
        for article in Post.query.all():
            for user in User.query.all():
                content = str(f"This is a comment for {article.title} from {user.name}")

                comment = Comment(
                    content=content,
                    post=article,
                    user=user,
                )

                if (
                    bool(
                        db.session.query(Comment)
                        .filter_by(content=content)
                        .first()
                    )
                    is False
                ):
                    db.session.add(comment)
                    db.session.commit()
                    logger.info(f"Added comment for {article.title}")
                else:
                    logger.info(f"Comment for {article.title} already exists")

        return app
