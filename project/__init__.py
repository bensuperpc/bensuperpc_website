from flask import Flask
from flask_login import LoginManager
from flask_paranoid import Paranoid
from flask_wtf.csrf import CSRFProtect
from loguru import logger

from .admin import admin as admin_blueprint
from .article import article as article_blueprint
from .auth import auth as auth_blueprint
from .db import Mutual, Post, User, db
from .main import main as main_blueprint
from .user import user as user_blueprint


def create_app(SECRET_KEY=None):
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
        return app
