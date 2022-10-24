from . import IdMixin, TimedMixin, User, db


class Comment(IdMixin, TimedMixin, db.Model):
    # title = db.Column(db.Text)
    content = db.Column(db.Text)

    # 0 = pending, 1 = approved, 2 = rejected
    status = db.Column(db.Integer, default=1)

    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    post = db.relationship("Post", back_populates="comments")

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="comments")

    def author(self):
        return self.user.username
