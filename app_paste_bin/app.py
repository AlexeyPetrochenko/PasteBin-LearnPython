from flask import Flask

from app_paste_bin.models import db


def create_app(config_filename='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)
    db.init_app(app)

    @app.route('/')
    def index():
        return f'Home Page'

    return app
