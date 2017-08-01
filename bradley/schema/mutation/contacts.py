import json
import graphene
from graphene import relay
from flask_security import current_user
from bradley.models import db, Contact, Pronouns
from bradley.schema.types import Pronouns as PronounsType
from bradley.schema.types import Contact as ContactType
from .input import PronounsInput, ContactNameInput, ContactEmailInput


def pronouns_from_dict(pronouns_dict):
    p = Pronouns.query.filter_by(**pronouns_dict).first()
    if not p:
        raise ValueError("Unknown pronouns: {json}".format(
            json=json.dumps(pronouns_dict)
        ))
    return p


class CreateContact(relay.ClientIDMutation):
    """
    Mutation to register a new user
    """
    class Input:
        pronouns = graphene.Field(PronounsInput)
        pronouns_list = graphene.List(PronounsInput)
        name = graphene.String()
        names = graphene.List(ContactNameInput)
        email = graphene.String()
        emails = graphene.List(ContactEmailInput)

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

        pronouns = input.get('pronouns', None)
        pronouns_list = [p for p in input.get('pronouns_list', []) if p]
        name = input.get('name', None)
        names = input.get('name_list', [])
        email = input.get('email', None)
        emails = input.get('emails', [])

        # we need at least one set of pronouns, at least one name,
        # and at least one email.
        errors = []
        if not pronouns and not pronouns_list:
            errors.append("At least one set of pronouns is required.")
        if pronouns:
            try:
                pronouns = pronouns_from_dict(pronouns)
            except ValueError as err:
                errors.append(err.args[0])
        if pronouns_list:
            try:
                pronouns_list = [pronouns_from_dict(d) for d in pronouns_list]
            except ValueError as err:
                errors.append(err.args[0])

        if not input.get('name') and not input.get('names'):
            errors.append("At least one name is required.")
        if not input.get('email') and not input.get('emails'):
            errors.append("At least one email address is required.")
        if errors:
            return CreateContact(
                success=False,
                errors=errors,
            )

        contact = Contact(user=current_user)
        if pronouns:
            contact.pronouns = pronouns
        if pronouns_list:
            contact.pronouns_list = pronouns_list

        if name:
            contact.name = name
        if names:
            for name_info in names:
                contact.names[name_info['category']] = name_info['name']

        if email:
            contact.email = email
        if emails:
            for email_info in emails:
                contact.emails[email_info['category']] = email_info['email']

        db.session.add(contact)
        db.session.commit()

        return CreateContact(
            success=True,
            contact=contact,
        )
