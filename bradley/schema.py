import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from bradley import models
from flask_security import current_user


class User(SQLAlchemyObjectType):
    class Meta:
        model = models.User
        interfaces = (relay.Node, )
        exclude_fields = ('password',)


class Role(SQLAlchemyObjectType):
    class Meta:
        model = models.Role
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    me = graphene.Field(User)
    all_users = SQLAlchemyConnectionField(User)
    all_roles = SQLAlchemyConnectionField(Role)

    def resolve_me(self, args, context, info):
        if current_user.is_authenticated:
            return current_user
        return None


schema = graphene.Schema(query=Query, types=[User, Role])
