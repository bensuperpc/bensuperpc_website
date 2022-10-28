#!/usr/bin/env python

import datetime
import io
import random
from sys import prefix

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from flask import (
    Blueprint,
    Response,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from loguru import logger
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from .db import Comment, Letter, Mutual, Post, User, db

admin = Blueprint(
    "admin",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/",
    url_prefix="/admin",
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
        "admin/dashboard.html",
        users_count=users_count,
        posts_count=posts_count,
        comments_count=comments_count,
        letters_count=letters_count,
        mutuals_count=mutuals_count,
        unread_letters_count=unread_letters_count,
        user_count_google=user_count_google,
    )


@admin.route("/plot/<string:plot_url>", methods=["GET"])
@login_required
def plot(plot_url):
    logger.debug(
        f"User {current_user.name} ({current_user.email}) is viewing the plot {plot_url}"
    )
    if current_user.admin is False:
        flash("Sorry, you don't have permission to read a letter.", "danger")
        return redirect(url_for("main.index"))

    if plot_url == "plot1" or plot_url == "plot1.png":
        fig = comment_count_plot()
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype="image/png")
    elif plot_url == "plot2" or plot_url == "plot2.png":
        fig = create_figure()
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype="image/png")

    flash("Sorry, this plot does not exist.", "danger")
    return redirect(url_for("main.index"))


# Generate plot with matplotlib, evolution of number of comments count since last 30 days
def comment_count_plot():
    logger.warning("Generating plot..")
    comments = Comment.query.filter(
        Comment.created > datetime.datetime.now() - datetime.timedelta(days=31)
    ).all()
    comments_count = np.zeros((31, 1), dtype=np.uint64)
    days = np.arange(1, 32)

    date = datetime.datetime.now() - datetime.timedelta(days=31)

    for i, comment in enumerate(comments):
        comment_date = comment.created
        day_index = (comment_date - date).days
        if comment_date >= date:
            comments_count[day_index] += 1

    plt.style.use("ggplot")

    fig = Figure()

    # fig, ax = plt.subplots()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(days, comments_count, color="blue", marker="o", linestyle="solid")

    ax.set_title("Evolution of number of comments since last 30 days")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of comments")

    fig.autofmt_xdate()
    ax.legend(title="Data")
    fig.tight_layout()

    return fig


def create_figure():
    plt.style.use("ggplot")
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig
