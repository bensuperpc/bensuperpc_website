from asyncio import tasks
import json
import os
from datetime import timedelta
import asyncio

from dotenv import load_dotenv
from flask import Flask, redirect, request
from flask_login import LoginManager
from flask_paranoid import Paranoid
from flask_wtf.csrf import CSRFProtect
from github3 import GitHub
from loguru import logger
from oauthlib.oauth2 import WebApplicationClient
from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash

# Import all blueprint
from .admin import admin as admin_blueprint
from .article import article as article_blueprint
from .auth import auth as auth_blueprint
from .db import Comment, Mutual, Post, User, db
from .letter import letter as letter_blueprint
from .main import main as main_blueprint
from .oauth import oauth
from .user import user as user_blueprint

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing

# https://stackoverflow.com/questions/7207309/how-to-run-functions-in-parallel
def add_articles(gh, item, lock = multiprocessing.Manager().Lock()):
    logger.debug(f"Adding article {item['title']}")
    content = None

    if item["from_github"] == True:
        content = gh.repository(item["user"], item["repository"]).file_contents(
            item["file"]
        )
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
    # Critical section (1 thread at a time)
    with lock:
        if (
            bool(db.session.query(Post).filter_by(
                title=item["title"]).first())
            is False
        ):

            db.session.add(post)
            db.session.commit()
            logger.debug(f"{post.title} added")
        else:
            logger.debug(f"{item['title']} already exists")
    logger.debug(f"Adding article {item['title']} done")


def create_app():

    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '.env'))

    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", None)
    GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID", None)
    GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET", None)

    SECRET_KEY = os.environ.get("SECRET_KEY")

    if GITHUB_TOKEN is None or GITHUB_CLIENT_ID is None or GITHUB_CLIENT_SECRET is None:
        logger.error(
            "GITHUB_TOKEN or GITHUB_CLIENT_ID or GITHUB_CLIENT_SECRET is not set, you need to set it in .env file")
        exit(1)

    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)

    if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
        logger.error(
            "GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET is not set, you need to set it in .env file")
        exit(1)

    app = Flask(__name__)

    app.config["SECRET_KEY"] = SECRET_KEY

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
    app.config['UPLOAD_FOLDER'] = 'uploads'

    app.config["REMEMBER_COOKIE_SECURE"] = True
    #app.config["REMEMBER_COOKIE_NAME"] = "remember_token"
    #app.config["REMEMBER_COOKIE_DOMAIN"] = "bensuperpc.com"

    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

    oauth.init_app(app)
    logger.info("OAuth initialized")
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={
            'scope': 'openid email profile',
            'prompt': 'select_account',
        }
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
        name='github',
        client_id=GITHUB_CLIENT_ID,
        client_secret=GITHUB_CLIENT_SECRET,
        access_token_url='https://github.com/login/oauth/access_token',
        access_token_params=None,
        authorize_url='https://github.com/login/oauth/authorize',
        authorize_params=None,
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'},
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

    db.init_app(app)
    logger.debug("App DB initialized")

    # Cookie protection
    paranoid = Paranoid(app)
    paranoid.redirect_view = "auth.login"

    # CSRF protection
    csrf = CSRFProtect()
    csrf.init_app(app)
    logger.debug("App CSRF initialized")

    # Login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    #login_manager.refresh_view = "accounts.reauthenticate"
    #login_manager.anonymous_user = MyAnonymousUser
    login_manager.session_protection = None  # Panaroid
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

    logger.debug(f"{app.name} is running on {app.config['ENV']}")

    with app.app_context():
        db.create_all()
        db.session.commit()

        gh = GitHub(token=GITHUB_TOKEN)

        # Add new articles for testing
        data = {}
        with open("project/static/data/article.json", encoding="UTF-8") as json_file:
            data = json.load(json_file)

        pool = ProcessPoolExecutor()
        m = multiprocessing.Manager()
        lock = m.Lock()
        futures = [pool.submit(add_articles, gh, item, lock) for item in data["articles"]]
        for future in futures:
            future.result()

        # Add new users only for testing
        logger.warning("Adding users, only for testing/dev !")
        data = {}
        with open("project/static/data/user.json", encoding="UTF-8") as json_file:
            data = json.load(json_file)

        for item in data["users"]:
            new_user = User(
                email=item["email"],
                name=item["name"],
                password=generate_password_hash(
                    item["password"], method="sha512"),
                admin=item["admin"],
                picture_url=item["picture_url"],
            )

            if (
                bool(db.session.query(User).filter_by(
                    email=item["email"]).first())
                is False
            ):
                db.session.add(new_user)
                db.session.commit()
                logger.info(f"{new_user.name} added")

        # Add mutuals for testing
        data = {}
        with open("project/static/data/mutual.json", encoding="UTF-8") as json_file:
            data = json.load(json_file)

        for item in data["mutuals"]:
            mutual = Mutual(
                name=item["name"],
                describe=item["describe"],
                picture_url=item["picture_url"],
                website_url=item["website_url"],
                twitter_url=item["twitter_url"],
                discord_url=item["discord_url"],
                youtube_url=item["youtube_url"],
                github_url=item["github_url"],
            )

            if (
                bool(db.session.query(Mutual).filter_by(
                    name=item["name"]).first())
                is False
            ):
                db.session.add(mutual)
                db.session.commit()
                logger.info("Added mutual")

        # Add comments for testing
        #logger.warning("Adding comments only for testing")
        for article in Post.query.all():
            for user in User.query.all():
                content = str(
                    f"This is a comment for {article.title} from {user.name}")

                comment = Comment(
                    content=content,
                    post=article,
                    user=user,
                )

                logger.info(f"Added comment for {article.title}")

                db.session.add(comment)
                db.session.commit()
                logger.info("Added comment")

        return app
