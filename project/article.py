import flask_sqlalchemy as sqlalchemy
import loguru as logger
import markdown
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import current_user, login_required
from werkzeug.exceptions import abort

from . import db
from .models import Post

article = Blueprint("article", __name__)


@article.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        summarize = request.form["summarize"]

        if not title:
            flash("Title is required!")
        else:
            post = Post(title=title, content=content, summarize=summarize)
            db.session.add(post)
            db.session.commit()
            flash('"{}" was successfully created!'.format(post.title))
            return redirect(url_for("main.article"))

    return render_template("create.html")


@article.route("/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    if post is None:
        abort(404)
    post.content = markdown.markdown(
        post.content,
        extensions=[
            "extra",
            "admonition",
            "codehilite",
            "meta",
            "nl2br",
            "sane_lists",
            "smarty",
            "toc",
            "wikilinks",
        ],
    )
    return render_template("post.html", post=post)


@article.route("/<int:id>/edit", methods=("GET", "POST"))
@login_required
def edit(id):
    post = Post.query.get_or_404(id)

    if post is None:
        abort(404)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        summarize = request.form["summarize"]
        updated = sqlalchemy.func.now()

        if not title:
            flash("Title is required!")
        else:
            post.title = title
            post.content = content
            post.summarize = summarize
            db.session.commit()
            flash('"{}" was successfully edited!'.format(post.title))
            return redirect(url_for("main.article"))

    return render_template("edit.html", post=post)


@article.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):

    post = Post.query.get_or_404(id)
    if post is None:
        abort(404)

    db.session.delete(post)
    db.session.commit()
    flash('"{}" was successfully deleted!'.format(post.title))
    return redirect(url_for("main.article"))
