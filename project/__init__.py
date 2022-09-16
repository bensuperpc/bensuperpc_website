import json
import os

from dotenv import load_dotenv
from flask import Flask, redirect, request
from flask_login import LoginManager
from flask_paranoid import Paranoid
from flask_wtf.csrf import CSRFProtect
from github3 import GitHub
from loguru import logger
from werkzeug.security import check_password_hash, generate_password_hash

# Import all blueprint
from .admin import admin as admin_blueprint
from .article import article as article_blueprint
from .auth import auth as auth_blueprint
from .db import Mutual, Post, User, db
from .main import main as main_blueprint
from .user import user as user_blueprint


def create_app(SECRET_KEY=None):

    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '.env'))

    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
    SECRET_KEY = os.environ.get("SECRET_KEY")

    app = Flask(__name__)

    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config['UPLOAD_FOLDER'] = 'uploads'

    db.init_app(app)
    logger.debug("App DB initialized")

    # Cookie protection
    paranoid = Paranoid(app)
    paranoid.redirect_view = "/"

    # CSRF protection
    csrf = CSRFProtect()
    csrf.init_app(app)
    logger.debug("App CSRF initialized")

    # Login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(main_blueprint)

    app.register_blueprint(auth_blueprint)

    app.register_blueprint(user_blueprint)

    app.register_blueprint(article_blueprint)

    app.register_blueprint(admin_blueprint)

    logger.debug(f"{app.name} is running on {app.config['ENV']}")

    with app.app_context():
        db.create_all()
        db.session.commit()
        gh = GitHub(token=GITHUB_TOKEN)

        # Add new articles for testing
        data = {}
        with open("project/static/data/article.json", encoding="UTF-8") as json_file:
            data = json.load(json_file)

        for item in data["articles"]:

            # if item["from_github"] == True:
            content = gh.repository(item["user"], item["repository"]).file_contents(
                item["file"]
            )
            content = content.decoded.decode("utf-8")
            post = Post(
                title=item["title"],
                content=content,
                summarize=item["description"],
                is_markdown=True,
            )
            logger.debug(f"{post.title} added")

            if (
                bool(db.session.query(Post).filter_by(
                    title=item["title"]).first())
                is False
            ):
                db.session.add(post)
                db.session.commit()
                logger.info("Added post")

        # Add new users only for testing
        logger.warning("Adding admin user only for testing")
        new_user_admin = User(
            email="admin@admin.net",
            name="admin",
            password=generate_password_hash("admin", method="sha512"),
            admin=True,
        )
        if (
            bool(db.session.query(User).filter_by(
                email="admin@admin.net").first())
            is False
        ):
            db.session.add(new_user_admin)
            db.session.commit()
            logger.info("Added user")

        logger.warning("Adding base user only for testing")
        new_user_base = User(
            email="base@base.net",
            name="base",
            password=generate_password_hash("base", method="sha512"),
            admin=False,
        )
        if (
            bool(db.session.query(User).filter_by(
                email="base@base.net").first())
            is False
        ):
            db.session.add(new_user_base)
            db.session.commit()
            logger.info("Added user")

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
        return app
