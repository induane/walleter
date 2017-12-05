.. Documentation master file, created by
   sphinx-quickstart on Tue Jan 27 12:04:31 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Walleters documentation!
===================================
A tool for brute-forcing weak user selected bitcoin addresses. It reads in text
from files into a list and then moves over that list in a windowed manner,
checking to see if any of the generated wallets exist and have coins. If it
finds any it writes the wallet info to a file.

Contents:

.. toctree::
   :maxdepth: 2

   topics/manual
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
