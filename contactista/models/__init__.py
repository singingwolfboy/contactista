# The ordering of this file is a little strange, but it's intentional,
# in order to avoid circular dependencies. First, we do library imports.

from sqlalchemy_continuum import make_versioned
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic
from flask_security import Security

# Then we set up the data that the models depend on, like the `db` instance
# from Flask-SQLAlchemy.

make_versioned()
db = SQLAlchemy()
alembic = Alembic()
security = Security()

# Now we can import the models.

from contactista.models.auth import User, Role
from contactista.models.contacts import (
    Contact, ContactName, ContactPronouns, ContactEmail
)
from contactista.models.tag import Tag, ContactTag
from contactista.models.shared import Pronouns


def shell_context():
    """
    This function is called when you run `flask shell`. It makes sure that
    the models are already loaded in the shell context when you start it up.
    """
    return {
        "db": db,
        "User": User,
        "Role": Role,
        "Contact": Contact,
        "ContactName": ContactName,
        "ContactPronouns": ContactPronouns,
        "ContactEmail": ContactEmail,
        "Pronouns": Pronouns,
        "Tag": Tag,
        "ContactTag": ContactTag,
    }
