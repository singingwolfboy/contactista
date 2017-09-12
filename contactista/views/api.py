from flask import Blueprint
from flask_graphql import GraphQLView as BaseGraphQLView
from flask_login import current_user
from contactista.schema import schema


class GraphQLView(BaseGraphQLView):
    def get_root_value(self, request):
        return current_user


blueprint = Blueprint('api', __name__)
blueprint.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
    )
)
