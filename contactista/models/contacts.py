from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.associationproxy import association_proxy
from contactista.models import db
from contactista.models.auth import User
from contactista.models.shared import Pronouns
from contactista.models.util import CategoryMap


# relationship cascade, needed to allow deleting from category maps
cascade = "save-update, merge, delete, delete-orphan"


class Contact(db.Model):
    """
    A person in your contact book.
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User, backref=db.backref("contacts"))
    note = db.Column(
        db.Text,
        doc="Personal notes that the user made about this contact"
    )
    # `notes_format` should probably be SQLAlchemy-Utils `ChoiceType`,
    # but Graphene has a bug with converting `ChoiceType`,
    # so this is a String instead.
    # https://github.com/graphql-python/graphene-sqlalchemy/issues/9
    note_format = db.Column(
        db.String(20), default="text",
        doc="Markup format for notes field. One of: text, markdown"
    )
    contact_pronouns = db.relationship(
        "ContactPronouns",
        order_by="ContactPronouns.position",
        collection_class=ordering_list("position"),
        cascade=cascade,
    )
    pronouns_list = association_proxy(
        "contact_pronouns", "pronouns",
        creator=lambda p: ContactPronouns(pronouns=p),
    )
    contact_names = db.relationship(
        "ContactName",
        order_by="ContactName.position",
        collection_class=CategoryMap,
        cascade=cascade,
    )
    contact_names_list = db.relationship(
        "ContactName",
        order_by="ContactName.position",
        cascade=cascade,
    )
    names = association_proxy(
        "contact_names", "name",
        creator=lambda c, n: ContactName(category=c, name=n),
    )
    contact_emails = db.relationship(
        "ContactEmail",
        order_by="ContactEmail.position",
        collection_class=CategoryMap,
        cascade=cascade,
    )
    contact_emails_list = db.relationship(
        "ContactEmail",
        order_by="ContactEmail.position",
        cascade=cascade,
    )
    emails = association_proxy(
        "contact_emails", "email",
        creator=lambda c, e: ContactEmail(category=c, email=e),
    )
    tags = db.relationship(
        "ContactTag",
        order_by="ContactTag.position",
        cascade=cascade,
    )

    @property
    def pronouns(self):
        """
        The primary set of pronouns that this contact uses.
        """
        if not self.pronouns_list:
            return None
        return self.pronouns_list[0]

    @pronouns.setter
    def pronouns(self, value):
        self.pronouns_list = [value]

    @pronouns.deleter
    def pronouns(self):
        self.pronouns_list = []

    @property
    def name(self):
        """
        The primary name for this contact if it exists,
        or the first name in the name order if not.
        """
        if not self.names:
            return None
        if "primary" in self.names:
            return self.names["primary"]
        # Get the first name, as ordered by the `position` column.
        # `self.names` is an ordered dictionary, so iteration is ordered.
        return next(self.names.values())

    @name.setter
    def name(self, value):
        self.names["primary"] = value

    @property
    def email(self):
        """
        The primary email for this contact if it exists,
        or the first email in the email order if not.
        """
        if not self.emails:
            return None
        if "primary" in self.emails:
            return self.emails["primary"]
        # `self.emails` is an ordered dictionary, so iteration is ordered.
        return next(self.emails.values())

    @email.setter
    def email(self, value):
        self.emails["primary"] = value

    def __str__(self):
        if self.name:
            return self.name
        return "Contact #{id}".format(id=self.id)

    def __repr__(self):
        if isinstance(self.id, int):
            id = self.id
        else:
            id = "unsaved"
        if self.names:
            return "<Contact {id} {name!r}>".format(id=id, name=self.name)
        else:
            return "<Contact {id}>".format(id=id)


class ContactPronouns(db.Model):
    contact_id = db.Column(
        db.Integer, db.ForeignKey(Contact.id),
        primary_key=True,
    )
    pronouns_id = db.Column(
        db.Integer, db.ForeignKey(Pronouns.id),
        primary_key=True,
    )
    position = db.Column(
        db.Integer, db.Sequence('contact_pronouns_position'),
        nullable=False,
    )

    contact = db.relationship(Contact)
    pronouns = db.relationship(Pronouns)

    def __str__(self):
        return str(self.pronouns)

    def __repr__(self):
        return "<ContactPronouns {cid} {pronouns}>".format(
            cid=self.contact_id, pronouns=self.pronouns,
        )


class ContactName(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_id = db.Column(db.Integer, db.ForeignKey(Contact.id))
    category = db.Column(db.String(50))
    position = db.Column(
        db.Integer, db.Sequence('contact_name_position'),
        nullable=False,
    )

    contact = db.relationship(Contact)
    name = db.Column(db.Text, nullable=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<ContactName {cid} {category}={name!r}>".format(
            cid=self.contact_id, name=self.name, category=self.category
        )


class ContactEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_id = db.Column(db.Integer, db.ForeignKey(Contact.id))
    category = db.Column(db.String(50))
    position = db.Column(
        db.Integer, db.Sequence('contact_email_position'),
        nullable=False,
    )

    contact = db.relationship(Contact)
    email = db.Column(db.Text, nullable=False)

    def __str__(self):
        return self.email

    def __repr__(self):
        return "<ContactEmail {cid} {email!r} {category!r}>".format(
            cid=self.contact_id, email=self.email, category=self.category
        )
