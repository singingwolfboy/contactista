import json
import os
import pytest
from contactista import create_app
from contactista.models import db as _db, Role, Pronouns
from testing.postgresql import Postgresql

# http://spotofdata.com/flask-testing/

@pytest.fixture(scope='session')
def app():
    _app = create_app()
    with Postgresql() as postgresql:
        _app.config.update({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": postgresql.url(),
            "SECURITY_PASSWORD_HASH": "plaintext",
            "SECURITY_PASSWORD_SCHEMES": ['plaintext'],
            "SECURITY_HASHING_SCHEMES": ["plaintext"],
            "SECURITY_DEPRECATED_HASHING_SCHEMES": [],
        })
        ctx = _app.app_context()
        ctx.push()

        yield _app

        ctx.pop()


@pytest.fixture(scope='session')
def db(app):
    _db.init_app(app)
    _db.create_all()
    seed_database(_db.session)
    yield _db
    _db.drop_all()


@pytest.fixture(scope='function')
def session(db):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session_ = db.create_scoped_session(options=options)

    db.session = session_

    yield session_

    transaction.rollback()
    connection.close()
    session_.remove()


def seed_database(session):
    session.add(Role(name="superuser", description="Unlimited access"))

    pronouns_fixture_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "contactista",
        "fixtures",
        "pronouns.json",
    )
    with open(pronouns_fixture_path) as f:
        pronouns_list = json.load(f)

    pronouns_objs = [Pronouns(
        subject=line[0],
        object=line[1],
        possessive_determiner=line[2],
        possessive=line[3],
        reflexive=line[4],
    ) for line in pronouns_list]
    session.add_all(pronouns_objs)
    session.commit()

