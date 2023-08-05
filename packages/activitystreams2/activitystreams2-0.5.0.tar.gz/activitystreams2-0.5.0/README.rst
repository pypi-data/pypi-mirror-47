==================
Activity Streams 2
==================

|pipeline-badge| |coverage-badge| |docs-badge| |pypi-badge|

``activitystreams2`` is a python library for producing Activity Streams 2.0
content. It doesn‘t have a lot of features (no extensions) but aims to be give
correct results and be easy to understand.

At the moment, only supports writing activity streams.

Installing
==========

The recommended way of manually installing activitystreams2 is via pip

.. code-block:: shell

   pip3 install activitystreams2

Examples
========

.. code-block:: python

   import activitystreams2

   martin = activitystreams2.Actor(id='http://www.test.example/martin')
   activity = activitystreams2.Create(
       actor=martin,
       summary='Martin created an image',
       object='http://example.org/foo.jpg',
   )
   # do this to serialize it
   json_string = str(activity)



Caveats
=======

We completely don’t support extension types at the moment.

Alternatives
============

The only python Activity Streams 2 library I know of is `activipy
<https://pypi.org/project/activipy/>`_. It supports extension types, but it‘s
still pre-alpha and seems to have been forgotten.


.. |pipeline-badge| image:: https://gitlab.com/alantrick/activitystreams2/badges/master/pipeline.svg
   :target: https://gitlab.com/alantrick/activitystreams2/
   :alt: Build Status

.. |coverage-badge| image:: https://gitlab.com/alantrick/activitystreams2/badges/master/coverage.svg
   :target: https://gitlab.com/alantrick/activitystreams2/
   :alt: Coverage Status

.. |docs-badge| image:: https://img.shields.io/badge/docs-latest-informational.svg
   :target: `the documentation`_
   :alt: Documentation

.. |pypi-badge| image:: https://img.shields.io/pypi/v/activitystreams2.svg
   :target: https://pypi.org/project/activitystreams2/
   :alt: Project on PyPI

.. _the documentation: https://alantrick.gitlab.io/activitystreams2/

