from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from bradley import models


class User(SQLAlchemyObjectType):
    class Meta:
        model = models.User
        interfaces = (relay.Node, )
        exclude_fields = ('password',)


class Role(SQLAlchemyObjectType):
    class Meta:
        model = models.Role
        interfaces = (relay.Node, )
