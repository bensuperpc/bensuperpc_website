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

from . import db
from .models import User

user = Blueprint("user", __name__)


@user.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)


@user.route("/user/<int:user_id>")
@login_required
def post(user_id):
    user = User.query.get_or_404(user_id)
    if user is None:
        abort(404)
    return render_template("profile.html", user=user, name=current_user.name)


@user.route("/user")
@login_required
def article():
    users = User.query.all()
    logger.info(users)
    return render_template("user.html", users=users)
