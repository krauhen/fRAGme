.. _usage:

Usage
============

Use as package from cli
-----------------------

.. code-block:: bash

    $ python -m venv venv
    $ source venv/bin/activate
    (venv)$ pip install fRAGme

    # or set with export globally for all variables
    (venv)$ export ORIGIN=*
    (venv)$ export OPENAI_API_KEY=YOUR_OPENAI_API_KEY
    (venv)$ export DATA_PATH="./data"
    (venv)$ export HOST=0.0.0.0
    (venv)$ export PORT=8080
    (venv)$ export AUTH=True
    (venv)$ export SECRET_KEY=YOUR_SECRET
    (venv)$ export ADMIN_SECRET=YOUR_HASHED_SECRET
    (venv)$ uvicorn fRAGme.app:app --host $HOST --port $PORT

.. image:: _static/images/terminal_webservice_up.png
  :width: 800
  :alt: Screenshot of active webservice.

OpenApiSpec(OAS)
----------------

.. image:: _static/images/fastapi_docs.png
  :width: 1200
  :alt: OpenAPISpec(OAS).

ReDoc
-----

.. image:: _static/images/fastapi_redoc.png
  :width: 1200
  :alt: ReDoc.
