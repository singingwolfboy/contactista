import pytest
from bradley.models import db, User
from bradley.serializers import UserSerializer

pytestmark = pytest.mark.usefixtures("app")


def test_user_serializer_empty():
    serializer = UserSerializer()
    result = serializer.load({})
    assert result.errors


def test_user_serializer():
    serializer = UserSerializer()
    data = {
        "username": "abcde",
        "password": "hunter2"
    }
    result = serializer.load(data)
    assert not result.errors
    user = result.data
    assert isinstance(user, User)
    assert user.username == "abcde"
    assert user.verify_password("hunter2")

