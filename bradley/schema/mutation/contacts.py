import json
import graphene
from graphene import relay
from flask_security import current_user
from bradley.models import db, Contact
from bradley.schema.types import UserError
from bradley.schema.types import Contact as ContactType
from bradley.serializers import ContactSerializer
from .input import PronounsInput, ContactNameInput, ContactEmailInput

class CreateContact(relay.ClientIDMutation):
    """
    Mutation to register a new user
    """
    class Input:
        pronoun = graphene.String()
        pronouns = graphene.Field(PronounsInput)
        pronouns_list = graphene.List(PronounsInput)
        name = graphene.String()
        names = graphene.List(ContactNameInput)
        email = graphene.String()
        emails = graphene.List(ContactEmailInput)
        notes = graphene.String()
        notes_format = graphene.String()

    success = graphene.Boolean()
    errors = graphene.List(UserError)
    contact = graphene.Field(ContactType)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        if current_user.is_anonymous:
            return CreateContact(
                success=False,
                errors=[UserError(field="", message="Authentication required")]
            )

        result = ContactSerializer(exclude=['user']).load(input)
        if result.errors:
            return CreateContact(
                success=False,
                errors=UserError.from_marshmallow(result.errors)
            )

        contact = result.data
        contact.user = current_user
        db.session.add(contact)
        db.session.commit()

        return CreateContact(
            success=True,
            contact=contact,
        )
