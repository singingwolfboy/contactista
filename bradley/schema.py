import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from bradley.models.auth import User, Role


class User(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node, )


class Role(SQLAlchemyObjectType):
    class Meta:
        model = Role
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_users = SQLAlchemyConnectionField(User)
    all_roles = SQLAlchemyConnectionField(Role)
    role = graphene.Field(Role)


schema = graphene.Schema(query=Query, types=[User, Role])
