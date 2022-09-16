from . import IdMixin, TimedMixin, db


class Post(IdMixin, TimedMixin, db.Model):
    title = db.Column(db.Text)
    summarize = db.Column(db.Text)
    content = db.Column(db.Text)
    is_markdown = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
