from flask import Flask
from flask_migrate import Migrate

from app_paste_bin.db import db


def create_app(config_filename='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)
    db.init_app(app)

    migrate = Migrate(app, db)

    @app.route('/')
    def index():
        return f'Home Page'

    return app
