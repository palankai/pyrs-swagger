============
pyrs.swagger
============

.. image:: https://readthedocs.org/projects/pyrs-swagger/badge/?version=latest
    :target: https://readthedocs.org/projects/pyrs-swagger/?badge=latest
    :alt: Documentation Status

Project homepage: `<https://github.com/palankai/pyrs-swagger>`_

Documentation: `<http://pyrs-swagger.readthedocs.org/en/latest/>`_

Issue tracking: `<https://github.com/palankai/pyrs-swagger/issues>`_

What is this package for
------------------------

I've found `Swagger <http://swagger.io/>`_ a really useful tool for
documenting any API. Unfortunately I haven't found simple to use python package
to create swagger documents.
Swagger document actually is a JSON file. The specification is itself a JSON
file too. Goal of this project provide tools for create this schema.

I've created the `pyrs framework <https://github.com/palankai/pyrs>`_ and
this work also part of it. The swagger document generation *can be*
based on `pyrs.resource <https://github.com/palankai/pyrs>`_ but not 
necessarily.

Nutshell
--------

.. code:: python

    from pyrs import swagger

    swagger = Swagger()

    # options are dictionary contains the endpoint information
    swagger.add('/user/', 'GET', options)
    swagger.add('/user/', 'POST', options)
    swagger.add('/user/<int: pk>', 'GET', options)
    swagger.add('/user/<int: pk>', 'PUT', options)
    swagger.add('/user/<int: pk>', 'DELETE', options)

    swaggerjsondoc = swagger.build()

If you are using the other parts of the framework, the building would be easier

.. code:: python

    from pyrs import swagger
    from pyrs import resource

    @GET(inject_app=True)
    def swagger(app):
        swagger = Swagger()
        swagger.discovery(app)
        return swagger.build()

    # in your pyrs application

    class MyAPI(resource.App):
        rwesources=(
            #...
            ('/swagger.json', swagger),
            #...
        )

    # then it should work magically


Features
--------

- Easy definition
- Schema validation
- Extensible API
- Auto generation

Installation
------------

The code is tested with python 2.7, 3.3, 3.4.

.. code:: bash

   $ pip install pyrs-swagger

Dependencies
------------

See `requirements.txt`. Right now (as it will be the first commit) the goal is
not define **any** hard dependency.

Important caveats
-----------------

This code is in beta version. I working hard on write stable as possible API in
the first place but while this code in 0.x version you should expect some major
modification on the API.

The ecosystem
-------------

This work is part of `pyrs framework <https://github.com/palankai/pyrs>`_.
The complete framework follow the same intention to implement flexible
solution.

Contribution
------------

I really welcome any comments!
I would be happy if you fork my code or create pull requests.
I've already really strong opinions what I want to achieve and how, though any
help would be welcomed.

Feel free drop a message to me!
