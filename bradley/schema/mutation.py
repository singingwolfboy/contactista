import graphene
from graphene import relay
from bradley import models
from bradley.jwt import jwt_token_for_user
from flask_security import login_user
from bradley.schema.types import User


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
                errors=['email', 'User account is disabled']
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


class Mutation(graphene.ObjectType):
    login = Login.Field()
