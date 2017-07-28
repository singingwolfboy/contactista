# The ordering of this file is a little strange, but it's intentional,
# in order to avoid circular dependencies. First, we import Flask-SQLAlchemy
# and initialize it.

from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
db = SQLAlchemy()
security = Security()

# All the application models depend on this `db` instance, so we can't
# import them until *after* we've initialized it. That's why the model
# imports come here.

from bradley.models.auth import User, Role


def shell_context():
    """
    This function is called when you run `flask shell`. It makes sure that
    the models are already loaded in the shell context when you start it up.
    """
    return {
        "User": User,
        "Role": Role,
    }
