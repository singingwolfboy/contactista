import pytest
from bradley.models import db, User, Contact
from bradley.serializers import UserSerializer, ContactSerializer

pytestmark = pytest.mark.usefixtures("app")


def test_user_serializer_empty():
    serializer = UserSerializer()
    result = serializer.load({})
    assert result.errors


def test_user_serializer(session):
    serializer = UserSerializer()
    data = {
        "username": "abcde",
        "password": "hunter2"
    }
    result = serializer.load(data)
    assert not result.errors
    user = result.data
    assert isinstance(user, User)
    session.add(user)
    session.commit()
    assert user.username == "abcde"
    assert user.verify_password("hunter2")


def test_contact_serializer_empty():
    serializer = ContactSerializer()
    result = serializer.load({})
    assert not result.errors
    contact = result.data
    assert isinstance(contact, Contact)
    assert contact.name is None
    assert contact.email is None


def test_contact_serializer(session):
    serializer = ContactSerializer()
    data = {
        "user": {
            "username": "testuser",
            "password": "testpass"
        },
        "name": "Jeeves",
        "email": "jeeves@butler.com",
        "pronoun": "he",
        "tags": ["butler"]
    }
    result = serializer.load(data)
    assert not result.errors
    contact = result.data
    assert isinstance(contact, Contact)
    session.add(contact)
    session.commit()
    assert contact.user.username == "testuser"
    assert contact.name == "Jeeves"
    assert contact.email == "jeeves@butler.com"
    assert contact.pronouns.subject == "he"
    assert contact.tags[0].name == "butler"


def test_contact_serializer_multiple_names(session):
    serializer = ContactSerializer()
    data = {
        "user": {
            "username": "testuser",
            "password": "testpass"
        },
        "names": [
            {"name": "Theo", "category": "nickname"},
            {"name": "David", "category": "first"},
            {"name": "Whatever", "category": "indecisive"},
        ],
        "emails": [
            {"email": "theo@earthlink.net", "category": "private"},
            {"email": "secret@mailinator.com", "category": "spam"},
            {"email": "professional+label@gmail.com", "category": "primary"},
        ],
        "pronouns_list": [
            {"subject": "he"},
            {"subject": "they", "reflexive": "themself"},
        ],
    }
    result = serializer.load(data)
    assert not result.errors
    contact = result.data
    assert isinstance(contact, Contact)
    session.add(contact)
    session.commit()
    assert contact.user.username == "testuser"
    assert contact.name == "Theo"  # first defined
    assert contact.names["indecisive"] == "Whatever"
    assert contact.email == "professional+label@gmail.com"  # primary category
    assert contact.emails["private"] == "theo@earthlink.net"
    assert contact.pronouns.subject == "he"
    assert contact.pronouns_list[1].subject == "they"
    assert not contact.tags
