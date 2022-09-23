from sys import prefix

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from loguru import logger

from .db import Comment, Letter, Mutual, Post, User, db

admin = Blueprint(
    "admin",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/",
)


@admin.route("/admin")
@login_required
def main_admin():
    logger.debug(
        f"User {current_user.name} ({current_user.email}) is viewing the admin page"
    )
    if current_user.admin is False:
        flash("Sorry, you don't have permission to access the admin panel.", "danger")
        logger.warning(
            f"User {current_user.name} ({current_user.email}) tried to log access admin panel"
        )
        return redirect(url_for("main.index"))

    return render_template("admin.html")


# https://getbootstrap.com/docs/5.2/examples/dashboard/
@admin.route("/dashboard")
@login_required
def dashboard():
    logger.debug(
        f"User {current_user.name} ({current_user.email}) is viewing the admin page"
    )
    if current_user.admin is False:
        flash("Sorry, you don't have permission to access the admin panel.", "danger")
        logger.warning(
            f"User {current_user.name} ({current_user.email}) tried to log access admin panel"
        )
        return redirect(url_for("main.index"))

    users_count = User.query.count()
    logger.info(f"Users count: {users_count}")

    user_count_google = User.query.filter_by(id_google=None).count()
    logger.info(f"Users count with Google: {user_count_google}")

    posts_count = Post.query.count()
    logger.info(f"Posts count: {posts_count}")

    comments_count = Comment.query.count()
    logger.info(f"Comments count: {comments_count}")

    letters_count = Letter.query.count()
    logger.info(f"Letters count: {letters_count}")

    mutuals_count = Mutual.query.count()
    logger.info(f"Mutuals count: {mutuals_count}")

    unread_letters_count = Letter.query.filter_by(is_read=False).count()
    logger.info(f"Unread letters: {unread_letters_count}")

    return render_template(
        "dashboard.html",
        users_count=users_count,
        posts_count=posts_count,
        comments_count=comments_count,
        letters_count=letters_count,
        mutuals_count=mutuals_count,
        unread_letters_count=unread_letters_count,
        user_count_google=user_count_google,
    )
