#!/usr/bin/env python

from argparse import ArgumentParser
from dotenv import load_dotenv
from loguru import logger
from website import create_app
import os


if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))

    debug = os.environ.get("FLASK_DEBUG", True)

    app = create_app()
    #app.run(host="0.0.0.0", port=5000, debug=debug, ssl_context=(os.path.join(basedir, "cert.pem"), os.path.join(basedir, "key.pem")))
    app.run(host="0.0.0.0", port=8080, debug=debug)
