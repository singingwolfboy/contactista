import graphene
from graphene import relay
from bradley import models
from bradley.jwt import (
    jwt_token_for_user, jwt_token_from_request, refresh_jwt_token
)
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
    error = graphene.List(graphene.String)
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
                error=['email', 'No user exists for that email address']
            )
        if not user.active:
            return Login(
                success=False,
                error=['email', 'User account is disabled']
            )
        if not user.verify_password(input['password']):
            return Login(
                success=False,
                error=['password', 'Invalid password']
            )
        # Login was successful!
        login_user(user)
        return Login(
            success=True,
            token=jwt_token_for_user(user).decode('utf8'),
            user=user,
        )


class RefreshToken(relay.ClientIDMutation):
    """
    Mutation to refresh a JWT token
    """
    class Input:
        pass
    success = graphene.Boolean()
    error = graphene.String()
    token = graphene.String()
    user = graphene.Field(User)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        token = jwt_token_from_request(context)
        if not token:
            return RefreshToken(
                success=False,
                error='Missing token',
            )
        try:
            new_token, user = refresh_jwt_token(token)
        except ValueError as err:
            message = err.args[0]
            return RefreshToken(
                success=False,
                errors=[message],
            )
        return Login(
            success=True,
            token=new_token.decode('utf8'),
            user=user,
        )


class Mutation(graphene.ObjectType):
    login = Login.Field()
    refresh_token = RefreshToken.Field()
