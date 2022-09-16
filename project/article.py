import flask_sqlalchemy as sqlalchemy
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
from loguru import logger
from werkzeug.exceptions import abort

# from . import db
from .db import Post, db
from .forms.post import PostForm

article = Blueprint(
    "article",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/",
)


@article.route("/article")
def panel():
    posts = Post.query.all()

    # Remove unpublished posts
    if current_user.admin is False:
        posts = [post for post in posts if post.is_published]

    return render_template("article.html", posts=posts)


@article.route("/post/create", methods=("GET", "POST"))
@login_required
def create():

    form = PostForm(request.form)
    form.is_published.checked = True

    if form.validate_on_submit():

        if current_user.admin is False:
            flash("Sorry, you don't have permission to create a post.")
            logger.warning(
                f"User {current_user.name} ({current_user.email}) tried to create a post"
            )
            return render_template("create.html", form=form)

        title = form.title.data
        summary = form.summary.data
        content = form.content.data
        is_markdown = form.is_markdown.data
        is_published = form.is_published.data

        post = Post(title=title, content=content, summarize=summary, is_markdown=is_markdown, is_published=is_published)
        db.session.add(post)
        db.session.commit()
        flash('"{}" was successfully created!'.format(post.title))
        return redirect(url_for("article.panel"))

    return render_template("create.html", form=form)


@article.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    if post is None:
        abort(404)
    if post.is_markdown:
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

    if post.is_published is False:
        flash("Post not found")
        abort(404)

    return render_template("post.html", post=post)


@article.route("/post/<int:id>/edit", methods=("GET", "POST"))
@login_required
def edit(id):
    post = Post.query.get_or_404(id)

    if post is None:
        abort(404)

    form = PostForm(request.form)

    if form.validate_on_submit():

        if current_user.admin is False:
            flash("Sorry, you don't have permission to edit a post.")
            logger.warning(
                f"User {current_user.name} ({current_user.email}) tried to edit a post"
            )
            return render_template("edit.html", form=form, post=post)

        post.title = form.title.data
        post.content = form.content.data
        post.summarize = form.summary.data
        post.updated = db.func.now()
        db.session.commit()
        flash('"{}" was successfully edited!'.format(post.title))
        return redirect(url_for("article.panel"))

    form.title.data = post.title
    form.content.data = post.content
    form.summary.data = post.summarize

    return render_template("edit.html", form=form, post=post)


@article.route("/post/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):

    post = Post.query.get_or_404(id)
    if post is None:
        abort(404)

    if current_user.admin is False:
        flash("Sorry, you don't have permission to delete a post.")
        return redirect(url_for("article.panel"))

    db.session.delete(post)
    db.session.commit()
    flash('"{}" was successfully deleted!'.format(post.title))
    return redirect(url_for("article.panel"))
