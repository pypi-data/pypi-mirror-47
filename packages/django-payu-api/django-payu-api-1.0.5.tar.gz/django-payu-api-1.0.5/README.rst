PAYU API
============

.. image:: https://img.shields.io/pypi/pyversions/intgr-bir-api.svg
    :target: https://pypi.python.org/pypi/intgr-bir-api/

.. image:: http://img.shields.io/pypi/v/intgr-bir-api.svg
    :target: https://pypi.python.org/pypi/intgr-bir-api/

.. image:: https://img.shields.io/badge/django-1.8%20or%20newer-green.svg
    :target: https://pypi.python.org/pypi/intgr-bir-api/

.. image:: https://img.shields.io/pypi/l/intgr-bir-api.svg
    :target: https://pypi.python.org/pypi/intgr-bir-api/

.. image:: https://img.shields.io/pypi/dm/intgr-bir-api.svg
    :target: https://pypi.python.org/pypi/intgr-bir-api/

An API for PayU allows integration with online payments using PayU.

Requirements
------------

payu-api requires Python 2.7 or Python 3.3 or newer and Django 1.11.

Installation
------------

To install payu-api, run the following command inside this directory::

    python setup.py install
    
You can also install the package with a symlink, so that changes to the source files will be immediately available to other users of the package on your system::

    python setup.py develop

If you have the Python **easy_install** utility available, you can also type 
the following to download and install in one step::

    easy_install intgr-payu-api

Or if you're using **pip**::

    pip install intgr-payu-api

To install payu-api from SVN directly::

    pip install -e svn+http://example.com/svn/intgr_bir_api/trunk#egg=bir_api
    
or, if you need install from branch::
    
    pip install -e svn+http://example.com/svn/intgr_bir_api/branches/dev_0_2#egg=bir_api

Or if you'd prefer you can simply place the included "payu_api" directory 
somewhere on your python path, or symlink to it from somewhere on your Python 
path.

Authors
-------

The project implemented by `Integree Bussines Solutions <http://www.integree.eu>`_ from Warsaw, Poland