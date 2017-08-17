import graphene


class PronounsInput(graphene.InputObjectType):
    subject = graphene.String()
    object = graphene.String()
    possessive_determiner = graphene.String()
    possessive = graphene.String()
    reflexive = graphene.String()


class ContactNameInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    category = graphene.String(required=True)


class ContactEmailInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    category = graphene.String(required=True)
