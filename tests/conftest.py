import pytest
from bradley import create_app
from bradley.models import db as _db
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
