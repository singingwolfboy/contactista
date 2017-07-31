import graphene
from bradley.schema.mutation.auth import Login, Register, RefreshToken
from bradley.schema.mutation.contacts import CreateContact


class Mutation(graphene.ObjectType):
    login = Login.Field()
    register = Register.Field()
    refresh_token = RefreshToken.Field()
    create_contact = CreateContact.Field()
