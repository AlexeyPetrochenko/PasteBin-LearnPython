from flask import Flask


def create_app(config_filename='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    @app.route('/')
    def index():
        return f'Home Page'

    return app

