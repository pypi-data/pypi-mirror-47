============
Installation
============


Stable release
--------------

To install pyhasse.fuzzy, run this command in your terminal:

.. code-block:: console

    $ pip install pyhasse.fuzzy

This is the preferred method to install pyhasse.fuzzy, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

From sources
------------

- Create a Python virtual environment.

.. code-block:: console

   python3 -m venv env

- Upgrade packaging tools.

.. code-block:: console

   env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

.. code-block:: console

   env/bin/pip install -e ".[testing]"

- Run your project's tests.

.. code-block:: console

   env/bin/pytest


The sources for pyhasse.fuzzy can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ hg clone ssh://hg@bitbucket.org/pyhasse/fuzzy

.. code-block:: console

    $ python setup.py develop


.. _Github repo: https://github.com/brg/fuzzy
.. _tarball: https://github.com/brg/fuzzy/tarball/master
