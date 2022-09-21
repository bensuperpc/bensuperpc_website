import os
import random

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
from werkzeug.utils import secure_filename

from .db import Letter, Mutual, Post, db
from .forms.contact import ContactForm
from .forms.upload import UploadForm

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
@main.route("/", subdomain="release")
@main.route("/")
def index():
    return render_template("index.html")


@main.route("/linktree")
def linktree():
    return render_template("linktree.html")


@main.route("/curriculum_vitae")
def curriculum_vitae():
    return render_template("curriculum_vitae.html")


@main.route("/mutual")
def mutual():
    mutuals = Mutual.query.all()
    random.shuffle(mutuals)
    return render_template("mutual.html", mutuals=mutuals)


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(main.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@main.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash("Thanks for contacting me!", "success")
        logger.info(f"Email: {form.email.data}: {form.message.data}")

        letter = Letter(
            email=form.email.data,
            message=form.message.data,
        )
        db.session.add(letter)
        db.session.commit()

        return redirect(url_for("main.index"))
    return render_template("contact.html", form=form)


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


@main.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        logger.info(f"User {current_user.name} is uploading a file.")

        files_filenames = []
        for file in form.files.data:
            if file.filename == "":
                flash(f"No selected file", "danger")
                return redirect(request.url)

            filename = secure_filename(file.filename)
            file.save(os.path.join(main.root_path, "uploads/", filename))
            files_filenames.append(filename)
        flash(f"Files uploaded: {files_filenames}", "success")
        return redirect(url_for("main.upload"))
    return render_template("upload.html", form=form)
