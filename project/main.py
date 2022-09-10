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

from .db import Mutual, Post

if __name__ == "__main__":
    logger.info("main.py")

main = Blueprint(
    "main",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/",
)


@main.route("/index")
@main.route("/main")
@main.route("/")
def index():
    return render_template("index.html")


@main.route("/linktree")
def linktree():
    return render_template("linktree.html")


@main.route("/mutual")
def mutual():
    mutuals = Mutual.query.all()
    return render_template("mutual.html", mutuals=mutuals)


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/article")
def article():
    posts = Post.query.all()
    logger.info(posts)
    return render_template("article.html", posts=posts)


@main.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(main.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@main.route("/share")
def share():
    musics_path = os.path.join(main.root_path, "static/media/music/")
    musics = os.listdir(musics_path)
    musics.remove(".gitkeep")
    logger.info(f"musics: {musics}")

    images_path = os.path.join(main.root_path, "static/media/image/")
    images = os.listdir(images_path)
    images.remove(".gitkeep")
    logger.info(f"images: {images}")

    videos_path = os.path.join(main.root_path, "static/media/video/")
    videos = os.listdir(videos_path)
    videos.remove(".gitkeep")
    logger.info(f"videos: {videos}")
    return render_template("share.html", musics=musics, images=images, videos=videos)


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