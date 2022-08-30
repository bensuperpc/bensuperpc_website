import json
import os

from dotenv import load_dotenv
from github3 import GitHub
from loguru import logger
from werkzeug.security import check_password_hash, generate_password_hash

from project import create_app, db
from project.models import Mutual, Post, User

if __name__ == "__main__":
    load_dotenv()
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    SECRET_KEY = os.getenv("SECRET_KEY")

    app = create_app(SECRET_KEY=SECRET_KEY)

    with app.app_context():

        gh = GitHub(token=GITHUB_TOKEN)

        # Add new articles for testing
        data = {}
        with open("project/static/data/article.json") as json_file:
            data = json.load(json_file)

        for item in data["articles"]:

            # if item["from_github"] == True:
            content = gh.repository(item["user"], item["repository"]).file_contents(
                item["file"]
            )
            content = content.decoded.decode("utf-8")
            post = Post(
                title=item["title"],
                content=content,
                summarize=item["description"],
            )
            logger.debug(f"{post.title} added")

            if (
                bool(db.session.query(Post).filter_by(title=item["title"]).first())
                is False
            ):
                db.session.add(post)
                db.session.commit()
                logger.info("Added post")

        # Add new users for testing
        new_user = User(
            email="admin@admin.net",
            name="admin",
            password=generate_password_hash("admin", method="sha512"),
            admin=True,
        )
        if (
            bool(db.session.query(User).filter_by(email="admin@admin.net").first())
            is False
        ):
            db.session.add(new_user)
            db.session.commit()
            logger.info("Added user")

        # Add mutuals for testing
        data = {}
        with open("project/static/data/mutual.json") as json_file:
            data = json.load(json_file)

        for item in data["mutuals"]:
            mutual = Mutual(
                name=item["name"],
                describe=item["describe"],
                picture_url=item["picture_url"],
                website_url=item["website_url"],
                twitter_url=item["twitter_url"],
                discord_url=item["discord_url"],
                youtube_url=item["youtube_url"],
                github_url=item["github_url"],
            )

            if (
                bool(db.session.query(Mutual).filter_by(name=item["name"]).first())
                is False
            ):
                db.session.add(mutual)
                db.session.commit()
                logger.info("Added mutual")

    app.run(host="0.0.0.0", port=5000, debug=True)
