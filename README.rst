====================
risclog.cryptography
====================

.. image:: https://github.com/risclog-solution/risclog.cryptography/workflows/Test/badge.svg?branch=master
     :target: https://github.com/risclog-solution/risclog.cryptography/actions?workflow=Test
     :alt: CI Status


.. image:: https://img.shields.io/pypi/v/risclog.cryptography.svg
        :target: https://pypi.python.org/pypi/risclog.cryptography

.. image:: https://img.shields.io/travis/risclog-solution/risclog.cryptography.svg
        :target: https://travis-ci.com/risclog-solution/risclog.cryptography

.. image:: https://readthedocs.org/projects/risclog.cryptography/badge/?version=latest
        :target: https://risclog.cryptography.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

Fernet guarantees that a message encrypted using it cannot be manipulated or read without the key. Fernet is an implementation of symmetric (also known as "secret key") authenticated cryptography. Fernet also has support for implementing key rotation via :class:`MultiFernet`.


* Free software: MIT license
* Documentation: https://risclog.cryptography.readthedocs.io.


Features
--------

Run tests::

    $ ./pytest









Credits
-------

This package was created with Cookiecutter_ and the `risclog-solution/risclog-cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`risclog-solution/risclog-cookiecutter-pypackage`: https://github.com/risclog-solution/risclog-cookiecutter-pypackage


This package uses AppEnv_ for running tests inside this package.

.. _AppEnv: https://github.com/flyingcircusio/appenv
