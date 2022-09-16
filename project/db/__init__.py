from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import sqlalchemy mixins
from .mixins import IdMixin, TimedMixin

# Import sqlalchemy models
from .letter import Letter
from .mutual import Mutual
from .post import Post
from .user import User

from .comment import Comment
