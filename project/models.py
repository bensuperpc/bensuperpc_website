import sqlalchemy as sa
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(256))
    admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password, method="sha512")

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    created = db.Column(db.DateTime, default=db.func.now())
    updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    content = db.Column(db.Text)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    summarize = db.Column(db.Text)


class Mutual(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    describe = db.Column(db.Text)
    picture_url = db.Column(db.String(256), default=None)
    website_url = db.Column(db.String(256), default=None)
    twitter_url = db.Column(db.String(256), default=None)
    discord_url = db.Column(db.String(256), default=None)
    youtube_url = db.Column(db.String(256), default=None)
    github_url = db.Column(db.String(256), default=None)
