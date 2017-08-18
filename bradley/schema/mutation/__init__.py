import graphene
from bradley.schema.mutation.auth import Login, Register, RefreshToken
from bradley.schema.mutation.contacts import (
    CreateContact, MutateContact, DestroyContact
)


class Mutation(graphene.ObjectType):
    login = Login.Field()
    register = Register.Field()
    refresh_token = RefreshToken.Field()
    create_contact = CreateContact.Field()
    mutate_contact = MutateContact.Field()
    destroy_contact = DestroyContact.Field()
