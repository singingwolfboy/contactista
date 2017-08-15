"""Shorter pronouns fields

Revision ID: 2fa884606f1a
Revises: ed99772734e1
Create Date: 2017-08-15 12:24:27.110853

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fa884606f1a'
down_revision = 'ed99772734e1'
branch_labels = ()
depends_on = None


def upgrade():
    for pronoun_type in ('possessive', 'subject', 'object', 'reflexive'):
        op.alter_column(
            table_name='pronouns',
            column_name='{pronoun_type}_pronoun'.format(pronoun_type=pronoun_type),
            new_column_name=pronoun_type,
        )


def downgrade():
    for pronoun_type in ('possessive', 'subject', 'object', 'reflexive'):
        op.alter_column(
            table_name='pronouns',
            column_name=pronoun_type,
            new_column_name='{pronoun_type}_pronoun'.format(pronoun_type=pronoun_type),
        )
