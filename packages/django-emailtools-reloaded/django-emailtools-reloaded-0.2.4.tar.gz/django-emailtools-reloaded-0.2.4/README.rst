==========================
django-emailtools-reloaded
==========================
``django-email-tools`` is a suite of tools meant to assist in sending emails
from your ``Django`` app.

.. image:: https://img.shields.io/pypi/v/django-emailtools-reloaded.svg
   :target: https://pypi.python.org/pypi/django-emailtools-reloaded
   :alt: PyPI Version

.. image:: https://travis-ci.org/barseghyanartur/django-emailtools-reloaded.png
   :target: http://travis-ci.org/barseghyanartur/django-emailtools-reloaded
   :alt: Build Status

.. image:: https://img.shields.io/badge/license-GPL--2.0--only%20OR%20LGPL--2.1--or--later-blue.svg
   :target: https://github.com/barseghyanartur/django-emailtools-reloaded/#License
   :alt: GPL-2.0-only OR LGPL-2.1-or-later

Prerequisites
=============
Python: 2.7, 3.5 and 3.6
Django: 1.8, 1.9, 1.10, 1.11, 2.0, 2.1 and 2.2

Installation
============
1.  Install the package:

    .. code-block:: sh

        pip install django-emailtools-reloaded

2.  Add ``emailtools`` to your ``INSTALLED_APPS``:

    .. code-block:: python

        INSTALLED_APPS = (
            # ...
            'emailtools',
            # ...
        )

Testing
=======
**Test current environment**

.. code-block:: sh

    ./runtests.py

**Test all environments**

.. code-block:: sh

    tox

Authors and maintainers
=======================
- Originally created and maintained at Fusionbox as ``django-emailtools``.
- Re-branded as ``django-emailtools-reloaded`` for better maintainability
  starting from May 2017.

Documentation
=============
See documentation `here <http://django-emailtools-reloaded.readthedocs.io/>`_.
