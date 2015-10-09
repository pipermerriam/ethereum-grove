.. Grove documentation master file, created by
   sphinx-quickstart on Wed Sep 30 12:46:03 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Grove's documentation!
=================================

Grove is an ethereum contract that provides an API for storing and retrieving
ordered data in a fast manner.

Grove indexes use an AVL tree for storage which has on average
``O(log n)`` time complexity for inserts and lookups.

Grove can be used as a library within your own contract, or as a service by
interacting with the publicly deployed Grove contract.

The Grove contract can be accessed at
``0x7d7ce4e2cdfea812b33f48f419860b91cf9a141d``.  If you would like to verify
the source, it was compiled using version ``0.1.3-1736fe80`` of the ``solc``
compiler with the ``--optimize`` flag turned on.


.. toctree::
   intro
   api
   library
   :maxdepth: 2

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
