from sqlalchemy import orm

from . import db


@orm.declarative_mixin
class IdMixin:
    id = db.Column(db.Integer, primary_key=True)


@orm.declarative_mixin
class TimedMixin:
    created = db.Column(db.DateTime, default=db.func.now())
    updated = db.Column(db.DateTime, default=db.func.now())
