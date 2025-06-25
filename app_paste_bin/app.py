from flask import Flask
# from flask_migrate import Migrate
from flask_login import LoginManager

from app_paste_bin.db import db
from app_paste_bin.post.views import blueprint as post_blueprint
from app_paste_bin.user.views import blueprint as user_blueprint
from app_paste_bin.user.models import User
from app_paste_bin.config import load_env


def create_app(config_filename='config.py'):
    app = Flask(__name__)
    config = load_env()

    # вручную скопировать нужные значения
    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URL

    db.init_app(app)

    app.register_blueprint(post_blueprint)
    app.register_blueprint(user_blueprint)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
