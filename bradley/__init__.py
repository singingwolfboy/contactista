from flask import Flask
from bradley.models import db, security, shell_context
from bradley.models.auth import user_datastore
from bradley.views.api import blueprint as api_bp
from bradley.admin import admin, admin_context
from bradley.jwt import user_from_jwt_request


DEFAULT_CONFIG = {
    "SECRET_KEY": "insecure-change-me",
    "SECURITY_PASSWORD_SALT": "insecure-change-me",
    "SQLALCHEMY_DATABASE_URI": "sqlite:///db.sqlite3",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "SECURITY_PASSWORD_HASH": "bcrypt",
}


def create_app():
    app = Flask(__name__)
    app.config.update(DEFAULT_CONFIG)
    db.init_app(app)
    state = security.init_app(app, datastore=user_datastore)
    state.login_manager.request_loader(user_from_jwt_request)
    state.context_processor(admin_context)
    admin.init_app(app)
    app.shell_context_processor(shell_context)
    app.register_blueprint(api_bp)
    return app
