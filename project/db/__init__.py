from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .letter import Letter
from .mixins import IdMixin, TimedMixin
from .mutual import Mutual
from .post import Post
from .user import User
