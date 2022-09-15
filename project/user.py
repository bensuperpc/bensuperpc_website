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

from .db import User, db

user = Blueprint("user", __name__)


@user.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)


@user.route("/user/<int:user_id>")
@login_required
def user_info(user_id):
    if (
        current_user.admin is False
        or current_user.id != user_id
        and current_user.admin is False
    ):
        flash("Sorry, you don't have permission to see user information.")
        logger.warning(
            f"User {current_user.name} ({current_user.email}) tried to see user information"
        )
        return redirect(url_for("main.index"))

    user = User.query.get_or_404(user_id)
    if user is None:
        abort(404)
    return render_template("profile.html", name=current_user.name)


@user.route("/user/<int:user_id>/enable_administrator", methods=["GET"])
@login_required
def enable_administrator(user_id):
    if not current_user.admin:
        flash("You don't have the permission to change user status", "danger")
        abort(403)

    user = db.session.query(User).get(user_id)
    if user is None:
        abort(404)
    user.admin = True
    db.session.commit()
    flash("User can now moderate", "success")
    return redirect(url_for("user.user_panel"))

@user.route("/user/<int:user_id>/disable_administrator", methods=["GET"])
@login_required
def disable_administrator(user_id):
    if not current_user.admin:
        flash("You don't have the permission to change user status", "danger")
        abort(403)
    
    if current_user.id == user_id:
        flash("You can't disable your own administrator status", "danger")
        return redirect(url_for("user.user_panel"))

    user = db.session.query(User).get(user_id)
    if user is None:
        abort(404)
    user.admin = False
    db.session.commit()
    flash("User can no longer moderate", "success")
    return redirect(url_for("user.user_panel"))


@user.route("/user")
@login_required
def user_panel():
    if current_user.admin is False:
        flash("Sorry, you don't have permission to see user list.")
        logger.warning(
            f"User {current_user.name} ({current_user.email}) tried to log access user panel"
        )
        return redirect(url_for("main.index"))

    users = User.query.all()
    logger.info(users)
    # TODO: add pagination and sorting
    # TODO: avoid to send all users information (ex hash password)
    return render_template("user.html", users=users)
