import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphene_sqlalchemy.utils import get_query
from bradley.schema.types import Tag, User, Contact, Pronouns
from flask_security import current_user


class CurrentUserConnectionField(SQLAlchemyConnectionField):
    @classmethod
    def get_query(cls, model, context, info, args):
        if current_user.is_anonymous:
            return []
        query = get_query(model, context)
        return query.filter(user=current_user)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    me = graphene.Field(User)
    tags = CurrentUserConnectionField(Tag)
    contacts = CurrentUserConnectionField(Contact)
    pronouns = SQLAlchemyConnectionField(Pronouns)

    def resolve_me(self, args, context, info):
        if current_user.is_authenticated:
            return current_user._get_current_object()
        return None
