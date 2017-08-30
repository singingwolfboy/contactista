import pytest
from colour import Color
from bradley.models import db, User, Contact, Tag
from bradley.jwt import jwt_token_for_user


def test_graphiql_enabled(client):
    resp = client.get("/graphql", headers={"Accept": "text/html"})
    assert resp.status_code == 200


@pytest.mark.usefixtures("session")
def test_anonymous_viewer(client):
    query = """
    {
      viewer {
        username
      }
    }
    """
    resp = client.get("/graphql", data={"query": query})
    assert resp.json == {
      "data": {
        "viewer": None,
      }
    }


@pytest.mark.usefixtures("session")
def test_empty_contacts(client):
    user = User(username="test")
    contact = Contact(user=user, name="Sally")
    db.session.add_all([user, contact])
    db.session.commit()
    query = """
    {
      viewer {
        contacts {
          edges {
            node {
              id
              name
            }
          }
        }
      }
    }
    """
    resp = client.get("/graphql", data={"query": query})
    assert resp.json == {
      "data": {
        "viewer": None,
      }
    }


@pytest.mark.usefixtures("session")
def test_basic_contacts(client):
    user1 = User(username="test")
    contact1 = Contact(user=user1, name="Sally")
    user2 = User(username="test2")
    contact2 = Contact(user=user2, name="Paul")
    db.session.add_all([user1, contact1, user2, contact2])
    db.session.commit()
    query = """
    {
      viewer {
        username
        contacts {
          edges {
            node {
              id
              name
            }
          }
        }
      }
    }
    """
    token = jwt_token_for_user(user1)
    headers = {"Authorization": "Bearer {token}".format(token=token.decode('utf-8'))}
    resp = client.get("/graphql", data={"query": query}, headers=headers)
    assert resp.json == {
      "data": {
        "viewer": {
          "username": "test",
          "contacts": {
            "edges": [{
              "node": {
                "id": "Q29udGFjdDo0",
                "name": "Sally",
              }
            }]
          }
        }
      }
    }


@pytest.mark.usefixtures("session")
def test_login(client, mocker):
    get_mock_token = mocker.patch(
      "bradley.schema.mutation.auth.jwt_token_for_user",
      return_value=b"faketoken",
    )
    user = User(username="test")
    user.set_password("abc")
    user.active = True
    db.session.add(user)
    db.session.commit()
    query = """
    mutation {
      login(input: {
        username: "test",
        password: "abc"
      }) {
        success
        errors {
          field
          message
        }
        token
        viewer {
          username
        }
      }
    }
    """
    resp = client.post("/graphql", data={"query": query})
    assert resp.json == {
      "data": {
        "login": {
          "success": True,
          "errors": [],
          "token": "faketoken",
          "viewer": {
            "username": "test"
          }
        }
      }
    }
    get_mock_token.assert_called_with(user)


@pytest.mark.usefixtures("session")
def test_create_tag(client):
    user = User(username="test")
    db.session.add(user)
    db.session.commit()
    assert Tag.query.filter_by(user=user).count() == 0
    query = """
    mutation {
      createTag(input: {
        name: "best conference",
        color: "#ff0000"
      }) {
        success
        errors {
          field
          message
        }
        tag {
          name
          color
        }
      }
    }
    """
    token = jwt_token_for_user(user)
    headers = {"Authorization": "Bearer {token}".format(token=token.decode('utf-8'))}
    resp = client.post("/graphql", data={"query": query}, headers=headers)
    assert resp.json == {
      "data": {
        "createTag": {
          "success": True,
          "errors": [],
          "tag": {
            "name": "best conference",
            "color": "#ff0000"
          }
        }
      }
    }
    assert Tag.query.filter_by(user=user).count() == 1
    tag = Tag.query.filter_by(user=user).first()
    assert tag.name == "best conference"
    assert isinstance(tag.color, Color)
    assert tag.color.hex == "#f00"
    assert tag.color.hex_l == "#ff0000"
