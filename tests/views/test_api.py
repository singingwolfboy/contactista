import pytest
from bradley.models import db, User


def test_graphiql_enabled(client):
    resp = client.get("/graphql", headers={"Accept": "text/html"})
    assert resp.status_code == 200


@pytest.mark.usefixtures("session")
def test_unauthorized_contacts(client):
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
