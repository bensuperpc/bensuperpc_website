#!/usr/bin/env python

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
from .db import Comment, Post, User, db
from .forms.comment import CommentForm
from .forms.post import PostForm

article = Blueprint(
    "article",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@article.route("/article")
def panel():
    posts = Post.query.all()

    # Remove unpublished posts
    if current_user.is_authenticated is False or current_user.admin is False:
        posts = [post for post in posts if post.is_published]

    return render_template("article.html", posts=posts)


@article.route("/post/create", methods=("GET", "POST"))
@login_required
def create():

    logger.debug(f"User {current_user.name} ({current_user.email}) is creating a post")

    form = PostForm(request.form)
    form.is_published.checked = True

    if form.validate_on_submit():

        if current_user.admin is False:
            flash("Sorry, you don't have permission to create a post.", "danger")
            logger.warning(
                f"User {current_user.name} ({current_user.email}) tried to create a post"
            )
            return render_template("create.html", form=form)

        title = form.title.data
        summary = form.summary.data
        content = form.content.data
        is_markdown = form.is_markdown.data
        is_published = form.is_published.data

        post = Post(
            title=title,
            content=content,
            summarize=summary,
            is_markdown=is_markdown,
            is_published=is_published,
        )
        db.session.add(post)
        db.session.commit()
        flash('"{}" was successfully created!'.format(post.title), "success")
        return redirect(url_for("article.panel"))

    return render_template("create.html", form=form)


@article.route("/post/<int:post_id>", methods=("GET", "POST"))
def post(post_id):

    form = CommentForm(request.form)

    post = Post.query.get_or_404(post_id)

    if post is None:
        flash("Post not found")
        abort(404)

    if post.is_published is False and current_user.admin is False:
        flash("Post is not published", "danger")
        redirect(url_for("article.panel"))

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

    if current_user.is_authenticated is True:
        logger.debug(
            f"User {current_user.name} ({current_user.email}) is viewing post {post_id}"
        )
    if form.validate_on_submit():

        post = Post.query.get_or_404(post_id)
        user = User.query.get_or_404(current_user.id)

        comment = Comment(
            content=form.content.data,
            post=post,
            user=user,
        )

        db.session.add(comment)
        db.session.commit()
        flash("Comment was successfully created!", "success")
        logger.debug(
            f"User {current_user.name} ({current_user.email}) is creating comment for post {post_id}"
        )
        return redirect(url_for("article.post", post_id=post_id))

    return render_template("post.html", post=post, form=form)


@article.route("/post/<int:id>/edit", methods=("GET", "POST"))
@login_required
def edit(id):
    logger.debug(
        f"User {current_user.name} ({current_user.email}) is editing post {id}"
    )
    if current_user.admin is False:
        flash("Sorry, you don't have permission to edit a post.", "danger")
        return redirect(url_for("article.panel"))

    post = Post.query.get_or_404(id)

    if post is None:
        flash("Post not found")
        abort(404)

    form = PostForm(request.form)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.summarize = form.summary.data
        post.updated = db.func.now()
        db.session.commit()
        flash('"{}" was successfully edited!'.format(post.title), "success")
        return redirect(url_for("article.panel"))

    form.title.data = post.title
    form.content.data = post.content
    form.summary.data = post.summarize

    return render_template("edit.html", form=form, post=post)


@article.route("/post/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    logger.debug(
        f"User {current_user.name} ({current_user.email}) is deleting post {id}"
    )

    if current_user.admin is False:
        flash("Sorry, you don't have permission to delete a post.")
        return redirect(url_for("article.panel"))

    post = Post.query.get_or_404(id)
    if post is None:
        abort(404)

    db.session.delete(post)
    db.session.commit()
    flash('"{}" was successfully deleted!'.format(post.title), "success")
    return redirect(url_for("article.panel"))


@article.route("/comments/<int:comment_id>/delete", methods=("GET",))
@login_required
def delete_comment(comment_id):
    if current_user.admin is False:
        flash("Sorry, you don't have permission to delete a comment.")
        return redirect(url_for("article.panel"))

    comment = Comment.query.get_or_404(comment_id)

    post_id = comment.post_id

    if comment.status == 2:
        flash("Comment is already deleted.", "danger")
        return redirect(url_for("article.post", post_id=post_id))

    comment.status = 2

    # db.session.delete(comment)
    db.session.commit()
    flash("Comment was successfully deleted!", "success")
    logger.debug(
        f"User {current_user.name} ({current_user.email}) is deleting comment {comment_id}"
    )
    return redirect(url_for("article.post", post_id=post_id))


@article.route("/comments/<int:comment_id>/edit", methods=("GET", "POST"))
@login_required
def edit_comment(comment_id):
    if current_user.admin is False:
        flash("Sorry, you don't have permission to edit a comment.", "danger")
        return redirect(url_for("article.panel"))

    comment = Comment.query.get_or_404(comment_id)
    db.session.commit()
    flash("Comment was successfully edited!", "success")
    logger.debug(
        f"User {current_user.name} ({current_user.email}) is editing comment {comment_id}"
    )
    return redirect(url_for("article.post", post_id=comment.post_id))
