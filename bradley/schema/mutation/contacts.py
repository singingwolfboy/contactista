import graphene
from graphene import relay
from flask_security import current_user
from bradley.models import db, Contact, ContactName, ContactPronouns, ContactEmail
from bradley.schema.types import Pronouns as PronounsType
from bradley.schema.types import Contact as ContactType
from bradley.schema.types import ContactName as ContactNameType
from bradley.schema.types import ContactEmail as ContactEmailType


class CreateContact(relay.ClientIDMutation):
    """
    Mutation to register a new user
    """
    class Input:
        names = graphene.List(ContactNameType, required=True)
        pronouns_ids = graphene.List(graphene.Int, required=True)
        emails = graphene.List(ContactEmailType, required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    contact = graphene.Field(ContactType)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        if current_user.is_anonymous:
            return CreateContact(
                success=False,
                errors=["Authentication required"]
            )
        contact = Contact(user=current_user)
        for name_info in input['names']:
            if isinstance(name_info, str):
                cn = ContactName(
                    name=name_info,
                    category="default",
                )
            else:
                cn = ContactName(
                    name=name_info['name'],
                    category=name_info['category'],
                )
            contact.contact_names.append(cn)
        for email_info in input['emails']:
            if isinstance(email_info, str):
                ce = ContactEmail(
                    email=email_info,
                    category="default",
                )
            else:
                ce = ContactEmail(
                    email=email_info['email'],
                    category=email_info['category'],
                )
            contact.contact_emails.append(ce)
        for pronouns_id in input['pronouns_ids']:
            cp = ContactPronouns(pronouns_id=pronouns_id)
            contact.contact_pronouns.append(cp)

        db.session.add(contact)
        db.session.commit()

        return CreateContact(
            success=True,
            contact=contact,
        )
