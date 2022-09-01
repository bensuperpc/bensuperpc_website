import os

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

from .models import Mutual, Post

if __name__ == "__main__":
    logger.info("main.py")

main = Blueprint("main", __name__)


@main.route("/index")
@main.route("/main")
@main.route("/")
def index():
    return render_template("index.html")


@main.route("/mutual")
def mutual():
    mutuals = Mutual.query.all()
    return render_template("mutual.html", mutuals=mutuals)


@main.route("/share")
def share():
    return render_template("share.html")


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/article")
def article():
    posts = Post.query.all()
    logger.info(posts)
    return render_template("article.html", posts=posts)


@main.route("/media/music/<path:filename>")
def upload_music(filename):
    uploads = os.path.join(main.root_path, "static/media/music/")
    return send_from_directory(uploads, filename, as_attachment=True)


@main.route("/media/image/<path:filename>")
def upload_image(filename):
    uploads = os.path.join(main.root_path, "static/media/image/")
    return send_from_directory(uploads, filename, as_attachment=True)


@main.route("/media/video/<path:filename>")
def upload_video(filename):
    uploads = os.path.join(main.root_path, "static/media/video/")
    return send_from_directory(uploads, filename, as_attachment=True)
