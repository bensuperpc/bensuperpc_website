from . import IdMixin, TimedMixin, db


class Post(IdMixin, TimedMixin, db.Model):
    title = db.Column(db.Text)
    summarize = db.Column(db.Text)
    content = db.Column(db.Text)
    picture_url = db.Column(
        db.Text,
        default="https://upload.wikimedia.org/wikipedia/commons/8/88/Bensuperpc_cat.jpg",
    )
    is_markdown = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=True)

    comments = db.relationship("Comment", back_populates="post")

    #def comment_count(self):
    #    return len(self.comments)

    def __repr__(self):
        return f"<Post {self.title}>"
