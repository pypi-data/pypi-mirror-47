.. _install:

#######################
Installing Numdifftools
#######################

We'll get started by setting up our environment.

************
Requirements
************

Numdifftools requires numpy 1.9 or newer, scipy 0.8 or newer, and Python 2.7 or 3.3 or newer. This tutorial assumes
you are using Python 3. Optionally you may also want to install Algopy 0.4 or newer and statsmodels 0.6 or newer in order 
to be able to use their easy to use interfaces to their derivative functions. 

************************
Your working environment
************************

We're going to assume that you have a reasonably recent version of virtualenv
installed and that you have some basic familiarity with it.


Create and activate a virtual environment
=========================================

::

    python3.6 -m venv env   # Python 2 usage: virtualenv env
    source env/bin/activate

Note that if you're using Windows, to activate the virtualenv you'll need::

    env\Scripts\activate


Update pip inside the virtual environment
=========================================

``pip`` is the Python installer. Make sure yours is up-to-date, as earlier versions can be less reliable::

	pip install --upgrade pip




Numdifftools installation
=========================

To install numdifftools, simply type::

    pip install djangocms-installer

to get the lastest stable version. Using pip also has the advantage that all requirements are automatically installed.


Unit tests
==========
To test if the toolbox is working paste the following in an interactive python session:

    import numdifftools as nd
    nd.test('--doctest-modules', '--disable-warnings')

If the result show no errors, you now have installed a fully functional toolbox. 
Congratulations!