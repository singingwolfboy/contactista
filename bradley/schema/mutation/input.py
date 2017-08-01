import graphene


class PronounsInput(graphene.InputObjectType):
    subject_pronoun = graphene.String()
    object_pronoun = graphene.String()
    possessive_determiner = graphene.String()
    possessive_pronoun = graphene.String()
    reflexive_pronoun = graphene.String()


class ContactNameInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    category = graphene.String(required=True)


class ContactEmailInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    category = graphene.String(required=True)
