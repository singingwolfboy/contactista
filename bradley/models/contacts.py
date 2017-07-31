from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import select, func
from bradley.models import db
from bradley.models.auth import User
from bradley.models.shared import Pronouns


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)
    notes = db.Column(db.Text)
    notes_format = db.Column(db.String(20), default="text")
    contact_names = db.relationship(
        "ContactName",
        order_by="ContactName.position",
        collection_class=ordering_list("position")
    )
    names = association_proxy("contact_names", "name")
    contact_pronouns = db.relationship(
        "ContactPronouns",
        order_by="ContactPronouns.position",
        collection_class=ordering_list("position")
    )
    pronouns = association_proxy("contact_pronouns", "pronouns")
    contact_emails = db.relationship(
        "ContactEmail",
        order_by="ContactEmail.position",
        collection_class=ordering_list("position")
    )
    emails = association_proxy("contact_emails", "email")

    def __str__(self):
        if self.names:
            return self.names[0]
        return "Contact #{id}".format(id=self.id)

    def __repr__(self):
        if isinstance(self.id, int):
            id = self.id
        else:
            id = "unsaved"
        if self.names:
            return "<Contact {id} {name!r}>".format(id=id, name=self.names[0])
        else:
            return "<Contact {id}>".format(id=id)


class ContactName(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(
        db.Integer, db.ForeignKey(Contact.id), nullable=False
    )
    contact = db.relationship(Contact)
    position = db.Column(db.Integer, nullable=False, default=0)

    name = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<ContactName {cid} {name!r} {category!r}>".format(
            cid=self.contact_id, name=self.name, category=self.category
        )


class ContactPronouns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(
        db.Integer, db.ForeignKey(Contact.id), nullable=False
    )
    contact = db.relationship(Contact)
    position = db.Column(db.Integer, nullable=False, default=0)

    pronouns_id = db.Column(
        db.Integer, db.ForeignKey(Pronouns.id), nullable=False
    )
    pronouns = db.relationship(Pronouns)

    def __str__(self):
        return str(self.pronouns)

    def __repr__(self):
        return "<ContactPronouns {cid} {pronouns}>".format(
            cid=self.contact_id, pronouns=self.pronouns,
        )


class ContactEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(
        db.Integer, db.ForeignKey(Contact.id), nullable=False
    )
    contact = db.relationship(Contact)
    position = db.Column(db.Integer, nullable=False, default=0)

    email = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return self.email

    def __repr__(self):
        return "<ContactEmail {cid} {email!r} {category!r}>".format(
            cid=self.contact_id, email=self.email, category=self.category
        )
