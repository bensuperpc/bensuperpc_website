from . import IdMixin, TimedMixin, db


class Letter(IdMixin, TimedMixin, db.Model):
    title = db.Column(db.Text)
    message = db.Column(db.Text)
    email = db.Column(db.Text)

    is_read = db.Column(db.Boolean, default=False)

    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
