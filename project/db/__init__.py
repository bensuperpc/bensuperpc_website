from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .mutual import Mutual
from .post import Post
from .user import User
