====
Aspy
====

|pipeline-badge| |coverage-badge| |docs-badge| |pypi-badge|

.. note:: Aspy has been renamed to
    `activitystreams2 <https://pypi.org/project/activitystreams2/>`_.


aspy is a python library for producing Activity Streams 2.0 content. It doesn‘t
have a lot of features (no extensions) but aims to be give correct results and
be easy to understand.

At the moment, only supports writing activity streams.

Examples
--------

.. code-block:: python

   import aspy

   martin = aspy.Actor(id='http://www.test.example/martin')
   activity = aspy.Create(
       actor=martin,
       summary='Martin created an image',
       object='http://example.org/foo.jpg',
   )
   # do this to serialize it
   json_string = str(activity)



Caveats
-------

We completely don't support extension types at the moment.

Alternatives
------------

The only python Activity Streams 2 library I know of is `activipy
<https://pypi.org/project/activipy/>`_. It supports extension types, but it‘s
still pre-alpha and seems to have been forgotten.


.. |pipeline-badge| image:: https://gitlab.com/alantrick/aspy/badges/master/pipeline.svg
   :target: https://gitlab.com/alantrick/aspy/
   :alt: Build Status

.. |coverage-badge| image:: https://gitlab.com/alantrick/aspy/badges/master/coverage.svg
   :target: https://gitlab.com/alantrick/aspy/
   :alt: Coverage Status

.. |docs-badge| image:: https://img.shields.io/readthedocs/aspy.svg
   :target: `the documentation`_
   :alt: Documentation

.. |pypi-badge| image:: https://img.shields.io/pypi/v/aspy.svg
   :target: https://pypi.org/project/aspy/
   :alt: Project on PyPI

.. _the documentation: http://aspy.readthedocs.io/en/latest/?badge=latest


Changes
=======

0.4.2
-----

* Add more name-change documentation

0.4.1
-----

* Document upcoming name change
* Drop PBR and switch to using a package

0.4
---

* Add rudimentary support for extension properties

0.3
---

* Fix bug printing collections with only 1 item

0.2.0
-----

* Add support for ActivityPub extension

0.1.0
-----

* Initial version


