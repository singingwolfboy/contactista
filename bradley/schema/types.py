import graphene
from graphene import relay, InputObjectType
from graphene_sqlalchemy import SQLAlchemyObjectType
from bradley import models


class User(SQLAlchemyObjectType):
    class Meta:
        model = models.User
        interfaces = (relay.Node,)
        exclude_fields = ('password',)


class Role(SQLAlchemyObjectType):
    class Meta:
        model = models.Role
        interfaces = (relay.Node,)


class Contact(SQLAlchemyObjectType):
    class Meta:
        model = models.Contact
        interfaces = (relay.Node,)


class Pronouns(SQLAlchemyObjectType):
    class Meta:
        model = models.Pronouns
        interfaces = (relay.Node,)


class ContactName(InputObjectType):
    name = graphene.String(required=True)
    category = graphene.String(required=True)


class ContactEmail(InputObjectType):
    email = graphene.String(required=True)
    category = graphene.String(required=True)

