from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from bradley.models import db, shell_context
from bradley.models.auth import user_datastore
from bradley.views.api import blueprint as api_bp


security = Security()


DEFAULT_CONFIG = {
    "SQLALCHEMY_DATABASE_URI": "sqlite:///db.sqlite3",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "SECURITY_PASSWORD_HASH": "bcrypt",
    "SECURITY_PASSWORD_SALT": "insecure-change-me",
}


def create_app():
    app = Flask(__name__)
    app.config.update(DEFAULT_CONFIG)
    db.init_app(app)
    security.init_app(app, datastore=user_datastore)
    app.shell_context_processor(shell_context)
    app.register_blueprint(api_bp)

    # inline import to avoid circular dependencies
    from bradley.manage import cli
    app.cli = cli

    return app
