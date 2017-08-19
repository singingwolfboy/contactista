import re
from marshmallow import fields, pre_load, post_load, validates, ValidationError
from marshmallow_sqlalchemy import ModelSchemaOpts, ModelSchema as BaseModelSchema
from marshmallow_sqlalchemy import field_for
from marshmallow_sqlalchemy.fields import get_schema_for_field
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from bradley.models import db
from bradley.models.auth import User, Role
from bradley.models.contacts import Contact, ContactName, ContactEmail, ContactPronouns
from bradley.models.tag import Tag, ContactTag
from bradley.models.shared import Pronouns


class BaseOpts(ModelSchemaOpts):
    def __init__(self, meta):
        if not hasattr(meta, 'sql_session'):
            meta.sqla_session = db.session
        super(BaseOpts, self).__init__(meta)


class ModelSchema(BaseModelSchema):
    OPTIONS_CLASS = BaseOpts


class SlugRelatedField(fields.Field):
    def __init__(self, column, create=None, **kwargs):
        self.column = column
        self.create = create
        super(SlugRelatedField, self).__init__(**kwargs)

    @property
    def session(self):
        schema = get_schema_for_field(self)
        return schema.session

    @property
    def model(self):
        schema = get_schema_for_field(self)
        return schema.opts.model

    @property
    def related_model(self):
        return getattr(self.model, self.attribute or self.name).property.mapper.class_

    def _serialize(self, value, attr, obj):
        return getattr(value, self.column)

    def _deserialize(self, value, attr, data):
        query = self.session.query(self.related_model)
        kwargs = {self.column: value}
        try:
            return query.filter_by(**kwargs).one()
        except NoResultFound:
            if self.create:
                return self.create(value)
            return self.related_model(**kwargs)


class RoleSerializer(ModelSchema):
    class Meta:
        model = Role


class UserSerializer(ModelSchema):
    password = field_for(User, 'password', required=True, load_only=True)
    roles = fields.List(SlugRelatedField('name'))

    class Meta:
        model = User
        exclude = ('contacts',)

    @validates('username')
    def validate_username(self, value):
        if not re.match(r"^[A-Za-z0-9_]+$", value):
            raise ValidationError("Invalid characters in username")

    @post_load
    def set_password(self, user):
        password = user.password
        user.set_password(password)
        return user


class PronounsSerializer(ModelSchema):
    class Meta:
        model = Pronouns


class ContactNameSerializer(ModelSchema):
    class Meta:
        model = ContactName
        fields = ('category', 'name')


class ContactEmailSerializer(ModelSchema):
    class Meta:
        model = ContactEmail
        fields = ('category', 'email')


class PronounsSerializer(ModelSchema):
    class Meta:
        model = Pronouns
        exclude = ('id', 'position')


class ContactPronounsSerializer(ModelSchema):
    pronouns = fields.Nested(PronounsSerializer)

    class Meta:
        model = ContactPronouns


class TagSerializer(ModelSchema):
    class Meta:
        model = Tag


class ContactTagSerializer(ModelSchema):
    name = field_for(Tag, 'name')
    color = field_for(Tag, 'color')

    class Meta:
        model = ContactTag
        fields = ('name', 'color', 'note')


def normalize_tag(data):
    if isinstance(data, str):
        return {"name": data}
    else:
        return data


class ContactSerializer(ModelSchema):
    user = fields.Nested(UserSerializer)
    names = fields.Nested(
        ContactNameSerializer,
        exclude=('contact',),
        many=True,
        attribute="contact_names_list",
    )
    emails = fields.Nested(
        ContactEmailSerializer,
        exclude=('contact',),
        many=True,
        attribute="contact_emails_list",
    )
    pronouns_list = fields.Nested(
        PronounsSerializer,
        many=True,
        attribute="pronouns_list",
    )
    tags = fields.Nested(
        ContactTagSerializer,
        many=True,
        attribute="tags",
    )

    class Meta:
        model = Contact
        fields = (
            'user', 'note', 'note_format',
            'names', 'emails', 'pronouns_list', 'tags',
        )

    @post_load(pass_original=True)
    def set_name(self, contact, original_data):
        name = original_data.get("name")
        if name:
            contact.name = name
        return contact

    @post_load(pass_original=True)
    def set_email(self, contact, original_data):
        email = original_data.get("email")
        if email:
            contact.email = email
        return contact

    @post_load(pass_original=True)
    def set_pronouns(self, contact, original_data):
        subject_pronoun = original_data.get("pronoun")
        if subject_pronoun:
            if not isinstance(subject_pronoun, str):
                raise ValidationError("Pronoun must be a string")
            contact.pronouns = get_pronouns_by_subject(subject_pronoun)

        filters = original_data.get("pronouns")
        if filters:
            if isinstance(filters, list) and all(isinstance(f, str) for f in filters):
                contact.pronouns_list = [get_pronouns_by_subject(f) for f in filters]
            elif isinstance(filters, dict):
                contact.pronouns = get_pronouns_by_filters(filters)
            else:
                raise ValidationError(
                    "Pronouns must be a list of subject pronoun strings, "
                    "or an object of pronoun types."
                )

        return contact

    @pre_load
    def normalize_tags(self, data):
        if data.get('tags'):
            data['tags'] = [normalize_tag(t) for t in data['tags']]
        return data


def get_pronouns_by_subject(subject_pronoun):
    """
    Given a subject pronoun (as a string), return the Pronouns object
    that corresponds to that subject pronoun. This can be called with
    strings like "he", "she", and "it".

    If no Pronouns object is found that matches this subject pronoun, or
    there are multiple Pronouns objects that match, a ValidationError is raised.
    """
    try:
        return Pronouns.query.filter_by(subject=subject_pronoun).one()
    except NoResultFound:
        raise ValidationError(
            'No set of pronouns found for subject pronoun "{subject}"'.format(
                subject=subject_pronoun
            )
        )
    except MultipleResultsFound:
        raise ValidationError(
            'Multiple sets of pronouns found for subject pronoun '
            '"{subject}". Use more specific filters.'.format(
                subject=subject_pronoun
            )
        )


def get_pronouns_by_filters(filters):
    """
    Given a dictionary of pronoun filters, return the Pronouns object
    that corresponds to those pronouns pronoun. Some examples:

    {"subject": "he"}
    {"subject": "they", "reflexive": "themself"}
    {"subject": "they", "reflexive": "themselves"}
    {"possessive": "hers"}

    If no Pronouns object is found that matches these filters, or
    there are multiple Pronouns objects that match, a ValidationError is raised.
    """
    try:
        return Pronouns.query.filter_by(**filters).one()
    except NoResultFound:
        raise ValidationError(
            "No set of pronouns found for filters."
        )
    except MultipleResultsFound:
        raise ValidationError(
            "Multiple sets of pronouns found. Use more specific filters."
        )


def shell_context():
    """
    This function is called when you run `flask shell`. It makes sure that
    the serializers are already loaded in the shell context
    when you start it up.
    """
    return {
        "UserSerializer": UserSerializer,
        "RoleSerializer": RoleSerializer,
        "ContactSerializer": ContactSerializer,
        "PronounsSerializer": PronounsSerializer,
        "TagSerializer": TagSerializer,
    }
