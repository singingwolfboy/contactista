from bradley.models import db
from flask_security import (
    UserMixin, RoleMixin, SQLAlchemyUserDatastore
)
from flask_security.utils import encrypt_password, verify_password


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def set_password(self, password):
        self.password = encrypt_password(password)

    def verify_password(self, password):
        return verify_password(password, self.password)

    def __str__(self):
        return self.username

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
