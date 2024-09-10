.. _docker:

Docker
======

From dockerhub
--------------

.. code-block:: bash

    docker pull krauhen/fragme
    docker run -d \
              --name fragme \
              --hostname fragme \
              --restart always \
              -p 8080:8080 \
              -e PORT=8080 \
              -e HOST=0.0.0.0 \
              -e OPENAI_API_KEY="" \
              -e AUTH=True \
              -e SECRET_KEY="YOUR_SECRET" \
              -e ADMIN_SECRET="YOUR_HASHED_SECRET" \
              krauhen/fragme:latest

.. image:: _static/images/terminal_docker_up.png
  :width: 800
  :alt: Screenshot of active docker webservice.

From source
-----------

.. code-block:: bash

    git clone git@github.com:krauhen/fRAGme.git
    cd fRAGme
    docker-compose build
    # set OPENAI_API_KEY in .env to "YOUR_OPENAI_API_KEY"
    docker-compose up

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

