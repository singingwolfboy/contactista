import graphene

# monkeypatch `graphene.relay.Connection` to support `totalCount`
class CountableConnection(graphene.relay.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int(
        description="Total number of items for connection"
    )

    @staticmethod
    def resolve_total_count(root, info):
        return root.length

graphene.relay.Connection = CountableConnection


from contactista.schema.types import User, Role, Contact, Pronouns, Tag
from contactista.schema.query import Query
from contactista.schema.mutation import Mutation


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    types=[User, Role, Contact, Pronouns, Tag]
)
