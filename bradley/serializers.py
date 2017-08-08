import re
from marshmallow import fields, post_load, validates, ValidationError
from marshmallow_sqlalchemy import ModelSchemaOpts, ModelSchema as BaseModelSchema
from marshmallow_sqlalchemy import field_for
from marshmallow_sqlalchemy.fields import get_schema_for_field
from sqlalchemy.orm.exc import NoResultFound
from bradley.models import db
from bradley.models.auth import User, Role


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


def shell_context():
    """
    This function is called when you run `flask shell`. It makes sure that
    the serializers are already loaded in the shell context
    when you start it up.
    """
    return {
        "UserSerializer": UserSerializer,
        "RoleSerializer": RoleSerializer,
    }
