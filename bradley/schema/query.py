import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from bradley.schema.types import User, Role, Contact, Pronouns
from flask_security import current_user


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    me = graphene.Field(User)
    all_users = SQLAlchemyConnectionField(User)
    all_roles = SQLAlchemyConnectionField(Role)
    contacts = SQLAlchemyConnectionField(Contact)
    pronouns = SQLAlchemyConnectionField(Pronouns)

    def resolve_me(self, args, context, info):
        if current_user.is_authenticated:
            return current_user._get_current_object()
        return None
