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

from .db import Letter, db
from .forms.contact import ContactForm

if __name__ == "__main__":
    logger.info("letter.py")

letter = Blueprint(
    "letter",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/",
    url_prefix="/",
)


@letter.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash("Thanks for contacting me!", "success")
        logger.info(f"Email: {form.email.data}: {form.message.data}")

        letter = Letter(
            email=form.email.data,
            message=form.message.data,
            title=form.title.data,
        )
        db.session.add(letter)
        db.session.commit()

        return redirect(url_for("main.index"))
    return render_template("contact.html", form=form)


@letter.route("/letters", methods=["GET"])
@login_required
def letters():
    if current_user.admin is False:
        flash("Sorry, you don't have permission to read a letter.")
        return redirect(url_for("main.index"))

    letters = Letter.query.all()
    return render_template("letter.html", letters=letters)


@letter.route("/read_letter/<int:letter_id>", methods=["GET"])
@login_required
def read_letter(letter_id):
    if current_user.admin is False:
        flash("Sorry, you don't have permission to read a letter.")
        return redirect(url_for("main.index"))

    letter = Letter.query.filter_by(id=letter_id).first_or_404()
    return render_template("read_letter.html", letter=letter)


@letter.route("/edit_letter/<int:letter_id>", methods=["GET", "POST"])
@login_required
def edit_letter(letter_id):
    if current_user.admin is False:
        flash("Sorry, you don't have permission to edit a letter.")
        return redirect(url_for("main.index"))

    letter = Letter.query.filter_by(id=letter_id).first_or_404()
    form = ContactForm()
    if form.validate_on_submit():
        letter.email = form.email.data
        letter.message = form.message.data
        letter.title = form.title.data
        db.session.commit()
        return redirect(url_for("main.letter"))
    elif request.method == "GET":
        form.email.data = letter.email
        form.message.data = letter.message
        form.title.data = letter.title
    return render_template("edit_letter.html", form=form)


@letter.route("/delete_letter/<int:letter_id>", methods=["GET"])
@login_required
def delete_letter(letter_id):
    if current_user.admin is False:
        flash("Sorry, you don't have permission to delete a letter.")
        return redirect(url_for("main.index"))

    letter = Letter.query.filter_by(id=letter_id).first_or_404()
    db.session.delete(letter)
    db.session.commit()
    return redirect(url_for("main.letter"))


@letter.route("/mark_read_letter/<int:letter_id>", methods=["GET"])
@login_required
def mark_read_letter(letter_id):
    if current_user.admin is False:
        flash("Sorry, you don't have permission to mark as read letter.")
        return redirect(url_for("main.index"))

    letter = Letter.query.filter_by(id=letter_id).first_or_404()
    letter.is_read = True
    db.session.commit()
    return redirect(url_for("main.letter"))
