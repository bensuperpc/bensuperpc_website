from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from .mixins import IdMixin, TimedMixin

from .letter import Letter
from .mutual import Mutual
from .post import Post
from .user import User
