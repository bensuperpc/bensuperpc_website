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

error = Blueprint(
    "error",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)

@error.app_errorhandler(404)
def handle_404(err):
    return render_template("404.html"), 404

