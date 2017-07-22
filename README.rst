Bradley
=======

Bradley is a Personal Relationship Management (PRM) system, similar to Monica_,
but written in Python.

Well, it isn't that *yet*. Right now, I'm just playing around with Flask_
and GraphQL_. But that's the eventual goal.

.. _Monica: https://monicahq.com/
.. _Flask: http://flask.pocoo.org/
.. _GraphQL: http://graphql.org/

Install & Run
-------------

.. code-block:: bash

    pip install -r requirements.txt
    export FLASK_APP=bradley/app.py
    flask db create
    flask run

You can run ``flask --help`` to see what other commands are available.
