import graphene
from graphene import relay, ObjectType, InputObjectType
from graphene.utils.trim_docstring import trim_docstring
from graphene_sqlalchemy import SQLAlchemyObjectType
from bradley import models


class UserError(ObjectType):
    """
    For displaying mutation errors to the user.
    """
    field = graphene.String()
    message = graphene.String()

    @classmethod
    def from_marshmallow(cls, errors):
        return [
            cls(field=field, message=message)
            for field, messages in errors.items()
            for message in messages
        ]


class User(SQLAlchemyObjectType):
    class Meta:
        model = models.User
        interfaces = (relay.Node,)
        exclude_fields = ('password',)


class Role(SQLAlchemyObjectType):
    class Meta:
        model = models.Role
        interfaces = (relay.Node,)


class Pronouns(SQLAlchemyObjectType):
    class Meta:
        model = models.Pronouns
        interfaces = (relay.Node,)


class ContactName(ObjectType):
    name = graphene.String()
    category = graphene.String()


class ContactEmail(ObjectType):
    email = graphene.String()
    category = graphene.String()


class Contact(SQLAlchemyObjectType):
    class Meta:
        model = models.Contact
        interfaces = (relay.Node,)

    # add relationships and proxies
    pronouns_list = graphene.Field(
        graphene.List(Pronouns),
        description=trim_docstring(models.Contact.pronouns_list.__doc__)
    )
    pronouns = graphene.Field(
        Pronouns,
        description=trim_docstring(models.Contact.pronouns.__doc__)
    )
    name = graphene.String(
        category=graphene.String(),
        description=trim_docstring(models.Contact.name.__doc__)
    )
    names = graphene.Field(
        graphene.List(ContactName),
        description=trim_docstring(models.Contact.contact_names_list.__doc__)
    )
    email = graphene.String(
        category=graphene.String(),
        description=trim_docstring(models.Contact.email.__doc__)
    )
    emails = graphene.Field(
        graphene.List(ContactEmail),
        description=trim_docstring(models.Contact.contact_names_list.__doc__)
    )

    def resolve_pronouns_list(self, args, context, info):
        return self.pronouns_list

    def resolve_pronouns(self, args, context, info):
        return self.pronouns

    def resolve_name(self, args, context, info):
        category = args.get('category')
        if category:
            return self.names.get(category, None)
        return self.name

    def resolve_names(self, args, context, info):
        return self.contact_names_list

    def resolve_email(self, args, context, info):
        category = args.get('category')
        if category:
            return self.emails.get(category, None)
        return self.email

    def resolve_emails(self, args, context, info):
        return self.contact_emails_list
