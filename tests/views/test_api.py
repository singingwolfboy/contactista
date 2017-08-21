import pytest
from bradley.models import db, User, Contact
from bradley.jwt import jwt_token_for_user


def test_graphiql_enabled(client):
    resp = client.get("/graphql", headers={"Accept": "text/html"})
    assert resp.status_code == 200


@pytest.mark.usefixtures("session")
def test_empty_contacts(client):
    query = """
    {
      contacts {
        edges {
          node {
            id
            name
          }
        }
      }
    }
    """
    resp = client.get("/graphql", data={"query": query})
    assert resp.json == {
      "data": {
        "contacts": {
          "edges": []
        }
      }
    }


@pytest.mark.usefixtures("session")
def test_unauthorized_contacts(client):
    user = User(username="test")
    contact = Contact(user=user, name="Sally")
    db.session.add_all([user, contact])
    db.session.commit()
    query = """
    {
      contacts {
        edges {
          node {
            id
            name
          }
        }
      }
    }
    """
    resp = client.get("/graphql", data={"query": query})
    assert resp.json == {
      "data": {
        "contacts": {
          "edges": []
        }
      }
    }


@pytest.mark.usefixtures("session")
def test_authorized_contacts(client):
    user = User(username="test")
    contact = Contact(user=user, name="Sally")
    db.session.add_all([user, contact])
    db.session.commit()
    query = """
    {
      contacts {
        edges {
          node {
            id
            name
          }
        }
      }
    }
    """
    token = jwt_token_for_user(user)
    headers = {"Authorization": "Bearer {token}".format(token=token.decode('utf-8'))}
    resp = client.get("/graphql", data={"query": query}, headers=headers)
    assert resp.json == {
      "data": {
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
