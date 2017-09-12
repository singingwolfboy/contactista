import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from contactista.schema.types import User, Pronouns
from flask_security import current_user


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    viewer = graphene.Field(User)
    pronouns = SQLAlchemyConnectionField(Pronouns)

    def resolve_viewer(self, info):
        if current_user.is_authenticated:
            return current_user._get_current_object()
        return None
