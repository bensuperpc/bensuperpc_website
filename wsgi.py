import json
import os

from dotenv import load_dotenv
from flask import redirect, request
from github3 import GitHub
from loguru import logger
from werkzeug.security import check_password_hash, generate_password_hash

from project import create_app
from project.db import Mutual, Post, User, db

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True, ssl_context=("cert.pem", "key.pem"))
