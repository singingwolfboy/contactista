import pytest
from bradley.models import db, User, Contact
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
