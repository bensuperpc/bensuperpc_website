from . import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    created = db.Column(db.DateTime, default=db.func.now())
    updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    content = db.Column(db.Text)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    summarize = db.Column(db.Text)
