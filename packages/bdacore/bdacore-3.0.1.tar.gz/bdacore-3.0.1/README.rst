===============
What is this?
===============

BDA core library of data science and data manipulation functions.

====================
How do I install it
====================

First, make sure you have miniconda or anaconda installed. If not, `install it! <https://conda.io/docs/user-guide/install/index.html>`_


Then you can install bdacore by running::

    make install

This will install the main requirements for running the bdacore lib. If you use advanced methods, you may need to
install extra packages.

If you want to install all required packages at once, then run::

    make develop_env

You may want to override the default package name (bdacore) and Python version (3.6). This can be done by overriding the *ENV_NAME* and *ENV_PY_VERSION* as follows::

    make develop_env ENV_NAME=bdacore_py2 ENV_PY_VERSION=2.7

===============================
Where can I see some examples?
===============================

Check the `docs <http://datadriver-doc-ddapi.s3-website-eu-west-1.amazonaws.com/bdacore/>`_. A good entry point is to check the `tutorials <http://datadriver-doc-ddapi.s3-website-eu-west-1.amazonaws.com/bdacore/tutorial.html>`_!
