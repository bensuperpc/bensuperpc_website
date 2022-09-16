from . import IdMixin, TimedMixin, db


class Letter(IdMixin, TimedMixin, db.Model):
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    email = db.Column(db.Text)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
