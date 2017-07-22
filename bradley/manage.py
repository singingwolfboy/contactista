import os
import click
from flask.cli import FlaskGroup
from flask_security.cli import users, roles
from bradley import create_app
from bradley.models import db as sa_db


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass

cli.add_command(users)
cli.add_command(roles)


@cli.group()
def db():
    "Manages the database."


@db.command()
def create():
    "Creates database tables."
    sa_db.create_all()


@db.command()
@click.confirmation_option(prompt="Are you sure you want to lose all your data?")
def drop():
    "Drops database tables."
    sa_db.drop_all()


if __name__ == '__main__':
    cli()
