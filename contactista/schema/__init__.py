import graphene
from contactista.schema.types import User, Role, Contact, Pronouns, Tag
from contactista.schema.query import Query
from contactista.schema.mutation import Mutation


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    types=[User, Role, Contact, Pronouns, Tag]
)
