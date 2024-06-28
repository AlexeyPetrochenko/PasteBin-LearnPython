from flask import Flask
from flask_migrate import Migrate

from app_paste_bin.db import db
from app_paste_bin.post.views import blueprint as post_blueprint


def create_app(config_filename='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(post_blueprint)

    return app
