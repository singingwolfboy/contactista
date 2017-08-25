Bradley Client
==============

This is the client application for Bradley. It is written in React_, and
interacts with the GraphQL API exposed by the server.

To build the client, you must first export the GraphQL schema defined in Flask,
and generate files with `Relay Compiler`_. Then you can use Webpack to build
the code. You'll need the following commands:

.. code-block::

    flask graphql schema client/data/schema.json
    yarn run relay
    yarn start

.. _Relay Compiler: https://facebook.github.io/relay/docs/relay-compiler.html
