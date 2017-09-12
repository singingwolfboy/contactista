from flask import Flask
from contactista.models import db, alembic, security
from contactista.models import shell_context as shell_context_models
from contactista.models.auth import user_datastore
from contactista.serializers import shell_context as shell_context_serializers
from contactista.views.api import blueprint as api_bp
from contactista.admin import admin, admin_context
from contactista.jwt import user_from_jwt_request
from contactista.cli import graphql


__version__ = "0.0.1"


DEFAULT_CONFIG = {
    "SECRET_KEY": "insecure-change-me",
    "SECURITY_PASSWORD_SALT": "insecure-change-me",
    "SQLALCHEMY_DATABASE_URI": "postgresql://localhost",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "SECURITY_PASSWORD_HASH": "bcrypt",
    "SECURITY_USER_IDENTITY_ATTRIBUTES": ["username"],
}


def create_app():
    app = Flask(__name__)
    app.config.update(DEFAULT_CONFIG)
    db.init_app(app)
    alembic.init_app(app)
    state = security.init_app(app, datastore=user_datastore)
    state.login_manager.request_loader(user_from_jwt_request)
    state.context_processor(admin_context)
    admin.init_app(app)
    app.shell_context_processor(shell_context_models)
    app.shell_context_processor(shell_context_serializers)
    app.register_blueprint(api_bp)
    app.cli.add_command(graphql, 'graphql')
    return app
