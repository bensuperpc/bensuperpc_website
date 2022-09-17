from . import IdMixin, db


class Mutual(IdMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    describe = db.Column(db.Text)
    picture_url = db.Column(db.String(256), default=None)
    website_url = db.Column(db.String(256), default=None)
    twitter_url = db.Column(db.String(256), default=None)
    discord_url = db.Column(db.String(256), default=None)
    youtube_url = db.Column(db.String(256), default=None)
    github_url = db.Column(db.String(256), default=None)
