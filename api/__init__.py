from flask import Flask
from config import Config

from api.view import main, login_manager
from api.model import db, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(main)

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "main.not_logged"
    return app
