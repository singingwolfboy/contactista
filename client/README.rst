Contactista Client
==================

This is the client application for Contactista. It is written in React_, and uses
Relay_ to interact with the GraphQL API exposed by the server.

To build the client, you must first export the GraphQL schema defined in Flask,
and generate files with `Relay Compiler`_. Then you can use Webpack to build
the code. You'll need the following commands:

.. code-block::

    flask graphql schema client/data/schema.json
    yarn run relay
    yarn start

.. _React: https://facebook.github.io/react/
.. _Relay: https://facebook.github.io/relay/
.. _Relay Compiler: https://facebook.github.io/relay/docs/relay-compiler.html
