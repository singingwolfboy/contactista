import click
import json
from contactista.schema import schema


@click.group()
def graphql():
    """GraphQL commands."""


@graphql.command('schema')
@click.argument('output', type=click.File('w'), default="schema.json")
@click.option(
    '--indent', default=None, type=int,
    help="Pretty-print at this indent level."
)
def graphql_schema(output, indent):
    """
    Output GraphQL schema. By default, this will save the schema to a file
    named "schema.json" in the current directory. To save the schema to a
    different file, pass the file path as an argument. To output the schema
    to stdout, pass "-" as an argument.
    """
    schema_dict = {"data": schema.introspect()}
    json.dump(schema_dict, output, indent=indent)
