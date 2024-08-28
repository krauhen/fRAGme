.. _usage:

Usage
============

Use as package from cli
-----------------------

.. code-block:: bash

    $ python -m venv venv
    $ source venv/bin/activate
    (venv)$ pip install fRAGme
    # set OPENAI_API_KEY in .env to "YOUR_OPENAI_API_KEY"
    (venv)$ uvicorn src.fRAGme.app:app --host 0.0.0.0 --port 8080

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
