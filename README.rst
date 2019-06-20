README
------

Installation Requirements
=========================

* Python 3.6+
* Dependencies: ``pip install -r requirements.txt``
* Run server: ``python manage.py runserver``
* Run tests: ``python manage.py test``

  * Note: This will print an exception even when all tests pass

Problem statement
=================

Build a URL shortening service, which includes a simple GraphQL API. The API
should provide the following functionality, and does not require any user
authentication:

- Submit a URL and get back a shortened URL. For example, submit
  ``http://www.google.ca/somelongpath`` and receive ``http://localhost/A7dw`` as
  the shortened URL
- Fetch the actual URL for a shortened tag. For example, passing in "A7dw" from
  the example above would return ``http://www.google.ca/somelongpath`` in the
  API response

In addition, visiting the shortened URL (e.g. ``http://localhost/A7dw`` from the
example above) would redirect the browser to the real URL.

Notes
=====

I haven't worked with GraphQL or graphene previously, so I may be missing some best practices.

A GraphiQL interface is available at ``http://localhost:8000/graphql/``

The short URL space has (26+26+10)^4 = 14,776,336 options, which is enough for a test but would have to be verified if it is large enough for production. As more URLs are generated, the collision detection means it will become more difficult to find a unique URL. This could be mitigated by having the same original URL always use the same short URL, but that leaks info that the URL has been used before (e.g. could look up the short URL being used on another site) and may not use fewer short URLs.

The API design is a little inconsistent since you can query by the short URL
(``A7dw``) but are still returned the full redirect (``http://localhost/A7dw``)
