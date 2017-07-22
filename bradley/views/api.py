from flask import Blueprint
from flask_graphql import GraphQLView
from bradley.schema import schema


blueprint = Blueprint('api', __name__)
blueprint.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)
