import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from bradley import models
from bradley.jwt import jwt_token_for_user
from flask_security import current_user, login_user


class User(SQLAlchemyObjectType):
    class Meta:
        model = models.User
        interfaces = (relay.Node, )
        exclude_fields = ('password',)


class Login(relay.ClientIDMutation):
    """
    Mutation to login a user
    """
    class Input:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    token = graphene.String()
    user = graphene.Field(User)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = (
            models.User.query
            .filter(models.User.email == input['email'])
            .scalar()
        )
        if not user:
            return Login(
                success=False,
                token=None,
                errors=['email', 'No user exists for that email address']
            )
        if not user.active:
            return Login(
                success=False,
                token=None,
                errors=['email', 'User is marked inactive, and is unable to log in']
            )
        if not user.verify_password(input['password']):
            return Login(
                success=False,
                token=None,
                errors=['password', 'Invalid password']
            )
        # Login was successful!
        login_user(user)
        return Login(
            success=True,
            token=jwt_token_for_user(user).decode('utf8'),
            errors=None,
            user=user,
        )


class Role(SQLAlchemyObjectType):
    class Meta:
        model = models.Role
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    me = graphene.Field(User)
    all_users = SQLAlchemyConnectionField(User)
    all_roles = SQLAlchemyConnectionField(Role)

    def resolve_me(self, args, context, info):
        if current_user.is_authenticated:
            return current_user._get_current_object()
        return None


class Mutation(graphene.ObjectType):
    login = Login.Field()


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    types=[User, Role]
)
