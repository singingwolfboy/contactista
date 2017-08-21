import pytest
import sqlalchemy as sa
from bradley.models import db, User


def test_username_unique(session):
    user1 = User(username="hhh")
    session.add(user1)
    session.commit()
    user2 = User(username="hhh")
    session.add(user2)
    with pytest.raises(sa.exc.IntegrityError):
        session.commit()
