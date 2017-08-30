import graphene
from graphene import ObjectType, InputObjectType
from graphene.relay import Node
from graphene.utils.trim_docstring import trim_docstring
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphene_sqlalchemy.converter import (
    convert_sqlalchemy_type, get_column_doc, is_column_nullable
)
from sqlalchemy_utils import ColorType
from bradley import models


@convert_sqlalchemy_type.register(ColorType)
def convert_column_to_string(type, column, registry=None):
    return graphene.String(
        description=get_column_doc(column),
        required=not(is_column_nullable(column)),
    )


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


class Pronouns(SQLAlchemyObjectType, interfaces=[Node]):
    class Meta:
        model = models.Pronouns
        description = trim_docstring(models.Pronouns.__doc__)


class Tag(SQLAlchemyObjectType, interfaces=[Node]):
    tag_id = graphene.Int()

    class Meta:
        model = models.Tag
        description = trim_docstring(models.Tag.__doc__)

    def resolve_tag_id(self, info):
        return self.id

    def resolve_color(self, info):
        return self.color.hex_l


class ContactName(ObjectType):
    name = graphene.String()
    category = graphene.String()


class ContactEmail(ObjectType):
    email = graphene.String()
    category = graphene.String()


class ContactTag(ObjectType):
    name = graphene.String()
    color = graphene.String()
    note = graphene.String()


class Contact(SQLAlchemyObjectType, interfaces=[Node]):
    contact_id = graphene.Int()
    note = graphene.String()
    note_format = graphene.String()

    class Meta:
        model = models.Contact
        description = trim_docstring(models.Contact.__doc__)

    def resolve_contact_id(self, info):
        return self.id

    def resolve_note(self, info):
        return self.note

    def resolve_note_format(self, info):
        return self.note_format

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
    tags = graphene.Field(
        graphene.List(ContactTag),
        description=trim_docstring(models.Contact.tags.__doc__)
    )

    def resolve_pronouns_list(self, info):
        return self.pronouns_list

    def resolve_pronouns(self, info):
        return self.pronouns

    def resolve_name(self, info, category=None):
        if category:
            return self.names.get(category, None)
        return self.name

    def resolve_names(self, info):
        return self.contact_names_list

    def resolve_email(self, info, category=None):
        if category:
            return self.emails.get(category, None)
        return self.email

    def resolve_emails(self, info):
        return self.contact_emails_list

    def resolve_tags(self, info):
        return self.tags


class Role(SQLAlchemyObjectType, interfaces=[Node]):
    role_id = graphene.Int()

    class Meta:
        model = models.Role

    def resolve_role_id(self, info):
        return self.id


class User(SQLAlchemyObjectType, interfaces=[Node]):
    user_id = graphene.Int()
    contacts = SQLAlchemyConnectionField(Contact)
    tags = SQLAlchemyConnectionField(Tag)

    class Meta:
        model = models.User
        exclude_fields = ('password',)
        description = trim_docstring(models.User.__doc__)

    def resolve_user_id(self, info):
        return self.id
