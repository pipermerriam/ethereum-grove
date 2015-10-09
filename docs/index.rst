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

The Grove Library can be used at the address
``0xd07ce4329b27eb8896c51458468d98a0e4c0394c``.

The Grove contract can be used at
``0x8017f24a47c889b1ee80501ff84beb3c017edf0b``.

If you would like to verify the source, it was compiled using version
``0.1.5-23865e39`` of the ``solc`` compiler with the ``--optimize`` flag turned
on.


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
