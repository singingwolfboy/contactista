import re
import graphene
from graphene import relay
from bradley.serializers import UserSerializer
from bradley.models import db, User
from bradley.jwt import (
    jwt_token_for_user, jwt_token_from_request, refresh_jwt_token
)
from flask_security import login_user
from bradley.schema.types import User as UserType, UserError


class Register(relay.ClientIDMutation):
    """
    Mutation to register a new user
    """
    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(UserError)
    token = graphene.String()
    viewer = graphene.Field(UserType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        result = UserSerializer().load(input)
        if result.errors:
            return cls(
                success=False,
                errors=UserError.from_marshmallow(result.errors),
            )
        user_exists = db.session.query(
            User.query.filter(User.username == input['username']).exists()
        ).scalar()
        if user_exists:
            return cls(
                success=False,
                errors=[UserError(
                    field="username", message="Username already in use"
                )]
            )
        user = result.data
        db.session.add(user)
        db.session.commit()
        return cls(
            success=True,
            token=jwt_token_for_user(user).decode('utf8'),
            viewer=user,
        )


class Login(relay.ClientIDMutation):
    """
    Mutation to login a user
    """
    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(UserError)
    token = graphene.String()
    viewer = graphene.Field(UserType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, *, username, password):
        user = (
            User.query
            .filter(User.username == username)
            .scalar()
        )
        if not user:
            return cls(
                success=False,
                errors=[
                    UserError('username', 'Specified user does not exist')
                ],
                token=None,
                viewer=None,
            )
        if not user.active:
            return cls(
                success=False,
                errors=[
                    UserError('username', 'Account is disabled')
                ],
                token=None,
                viewer=None,
            )
        if not user.verify_password(password):
            return cls(
                success=False,
                errors=[
                    UserError('password', 'Invalid password')
                ],
                token=None,
                viewer=None,
            )
        # Login was successful!
        login_user(user)
        return cls(
            success=True,
            errors=[],
            token=jwt_token_for_user(user).decode('utf8'),
            viewer=user,
        )


class RefreshToken(relay.ClientIDMutation):
    """
    Mutation to refresh a JWT token
    """
    success = graphene.Boolean()
    error = graphene.String()
    token = graphene.String()
    viewer = graphene.Field(UserType)

    @classmethod
    def mutate_and_get_payload(cls, root, info):
        token = jwt_token_from_request(context)
        if not token:
            return cls(
                success=False,
                error='Missing token',
            )
        try:
            new_token, user = refresh_jwt_token(token)
        except ValueError as err:
            message = err.args[0]
            return cls(
                success=False,
                error=message,
            )
        return cls(
            success=True,
            token=new_token.decode('utf8'),
            viewer=user,
        )
