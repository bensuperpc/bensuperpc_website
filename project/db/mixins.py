from email.policy import default
from enum import unique

from sqlalchemy import orm

from . import db


@orm.declarative_mixin
class IdMixin:
    id = db.Column(db.Integer, primary_key=True)


@orm.declarative_mixin
class IdGoogleMixin:
    id_google = db.Column(db.Integer, unique=True, nullable=True)


@orm.declarative_mixin
class IdGithubMixin:
    id_github = db.Column(db.Integer, unique=True, nullable=True)


@orm.declarative_mixin
class IdTwitterMixin:
    id_twitter = db.Column(db.Integer, unique=True, nullable=True)


@orm.declarative_mixin
class IdFacebookMixin:
    id_facebook = db.Column(db.Integer, unique=True, nullable=True)


@orm.declarative_mixin
class TimedMixin:
    created = db.Column(db.DateTime, default=db.func.now())
    updated = db.Column(db.DateTime, default=db.func.now())
