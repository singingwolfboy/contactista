import sqlalchemy as sa
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy_utils import ColorType
from colour import RGB_color_picker
from bradley.models import db
from bradley.models.auth import User
from bradley.models.contacts import Contact
from bradley.models.shared import Pronouns
from bradley.models.util import CategoryMap


def random_color(context):
    return RGB_color_picker(context.current_parameters['name'])


class Tag(db.Model):
    """
    A per-user tag, used for organizing contacts.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User, backref=db.backref("tags"))
    name = db.Column(db.String(80), nullable=False)
    color = db.Column(ColorType, default=random_color)

    __table_args__ = (
        db.UniqueConstraint(user_id, name),
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Tag {name}>".format(name=self.name)


class ContactTag(db.Model):
    """
    An association between a tag and a specific contact. This allows the user
    to make notes about why this tag belongs on this specific contact.
    """
    contact_id = db.Column(
        db.Integer, db.ForeignKey(Contact.id),
        primary_key=True,
    )
    tag_id = db.Column(
        db.Integer, db.ForeignKey(Tag.id),
        primary_key=True,
    )
    position = db.Column(
        db.Integer, db.Sequence('contact_tag_position'),
        nullable=False,
    )

    contact = db.relationship(Contact)
    tag = db.relationship(Tag)
    note = db.Column(db.Text)

    @property
    def name(self):
        if self.tag:
            return self.tag.name

    @name.setter
    def name(self, value):
        if self.tag:
            tag = self.tag
            tag.name = value
        else:
            tag = Tag(name=value)
        if self.contact and self.contact.user:
            self.tag = tag_with_user(tag, self.contact.user)
        else:
            self.tag = tag

    @property
    def color(self):
        if self.tag:
            return self.tag.color

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<ContactTag {contact} {tag}>".format(
            contact=self.contact, tag=self.tag,
        )


def tag_with_user(tag, user):
    """
    Given a tag and a user, return the Tag object in the database that matches
    the given name and the given user. If there is no Tag object in the
    database that matches, just set it on the existing object and return it.
    """
    if user is None or tag.user == user:
        # Nothing to do. Just return.
        return tag
    if user.id is None:
        # User hasn't been saved yet -- querying will raise a warning,
        # so just don't query.
        tag.user = user
        return tag
    # We have a user that doesn't match the given tag. See if we already
    # have a tag for the given name and user.
    try:
        return Tag.query.filter_by(name=tag.name, user=user).one()
    except NoResultFound:
        # Nope, we don't. This will be a newly-saved tag.
        tag.user = user
        return tag


# We use SQLAlchemy's event interface to ensure that
# the tag's user always matches the contact's user.

def user_set_listener(contact, user, old_user, initiator):
    for contact_tag in contact.tags:
        contact_tag.tag = tag_with_user(contact_tag.tag, user)

sa.event.listen(Contact.user, 'set', user_set_listener)

def contact_tag_append_listener(contact, contact_tag, initiator):
    # If the contact doesn't have a user set, nothing to do.
    if not contact.user:
        return

    # If the contact tag already has a user, make sure it's a match.
    if contact_tag.tag.user:
        if contact_tag.tag.user == contact.user:
            return
        else:
            raise ValueError(
                "User mismatch on appending tag. "
                "Contact user: {contact_user!r} "
                "Tag user: {tag_user!r}"
                .format(contact_user=contact.user, tag_user=contact_tag.tag.user)
            )

    # The contact has a user, and the contact tag does not. Set it.
    contact_tag.tag = tag_with_user(contact_tag.tag, contact.user)

sa.event.listen(Contact.tags, 'append', contact_tag_append_listener)
