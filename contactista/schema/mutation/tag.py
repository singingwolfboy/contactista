import json
import graphene
from graphene import relay
from flask_security import current_user
from sqlalchemy.exc import IntegrityError
from contactista.models import db, Tag
from contactista.schema.types import UserError
from contactista.schema.types import Tag as TagType
from contactista.serializers import TagSerializer

class CreateTag(relay.ClientIDMutation):
    """
    Mutation to create a new tag
    """
    class Input:
        name = graphene.String(required=True)
        color = graphene.String()

    success = graphene.Boolean()
    errors = graphene.List(UserError)
    tag = graphene.Field(TagType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if current_user.is_anonymous:
            return cls(
                success=False,
                errors=[UserError(field="", message="Authentication required")]
            )

        serializer = TagSerializer(exclude=['user'])
        result = serializer.load(input)

        if result.errors:
            return cls(
                success=False,
                errors=UserError.from_marshmallow(result.errors)
            )

        tag = result.data
        tag.user = current_user
        db.session.add(tag)

        try:
            db.session.commit()
        except IntegrityError:
            message = 'Tag with name "{name}" already exists'.format(
                name=tag.name
            )
            error = UserError(field="name", message=message)
            return cls(
                success=False,
                errors=[error],
            )

        return cls(
            success=True,
            errors=[],
            tag=tag,
        )


class MutateTag(relay.ClientIDMutation):
    """
    Mutation to modify an existing tag
    """
    class Input:
        tag_id = graphene.Int(required=True)
        name = graphene.String()
        color = graphene.String()

    success = graphene.Boolean()
    errors = graphene.List(UserError)
    tag = graphene.Field(TagType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if current_user.is_anonymous:
            return cls(
                success=False,
                errors=[UserError(field="", message="Authentication required")]
            )

        tag_id = input['tag_id']
        tag = Tag.query.get(tag_id)
        if not tag or tag.user != current_user:
            return cls(
                success=False,
                errors=[UserError(
                    field="tag_id",
                    message="Tag not found"
                )]
            )

        serializer = TagSerializer(exclude=['user'], partial=True)
        result = serializer.load(input, instance=tag)

        if result.errors:
            return cls(
                success=False,
                errors=UserError.from_marshmallow(result.errors)
            )

        db.session.add(result.data)
        db.session.commit()

        return cls(
            success=True,
            tag=tag,
        )


class DestroyTag(relay.ClientIDMutation):
    """
    Mutation to delete an existing tag
    """
    class Input:
        tag_id = graphene.Int(required=True)

    success = graphene.Boolean()
    errors = graphene.List(UserError)
    tag = graphene.Field(TagType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if current_user.is_anonymous:
            return cls(
                success=False,
                errors=[UserError(field="", message="Authentication required")]
            )

        tag_id = input['tag_id']
        tag = Tag.query.get(tag_id)
        if not tag or contact.user != current_user:
            return cls(
                success=False,
                errors=[UserError(
                    field="tag_id",
                    message="Tag not found"
                )]
            )

        db.session.delete(tag)
        db.session.commit()

        return cls(
            success=True,
            tag=tag,
        )
