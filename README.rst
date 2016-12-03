============
GitRdone4 Time Series Project
============

Final group project for Harvard's CS 207 course, Systems Development for Computational Science (Fall 2016).

Overview
========

Time series are two-dimensional (or higher) arrays of numeric data, where ordered time-values are bound to specific data points that represent specific outcomes, measurements, or other values associated with specific times. While time series data can be stored using traditional arrays or tables, the classes included in this library make working with these types of data sets in python easier by enforcing the core properties of a time series at a class level. For example, in a time series no two times can be repeated. And every represented value needs a time associated with it. By creating and manipulating data-sets using these classes, these properties are enforced at all times.

How to install
==============
1. Clone repo
2. Run:: python setup.py install

Additional Features
===================

1. Supports adding, subtracting, multiplying, and other manipulations on fixed-length data sets.
2. Support manipulation of time-series streams (i.e., data sets that are ongoing, and don't have fixed storage)
3. Supports piecewise linear interpolation of non-existing values within the domain of existing fixed-length data-sets.
4. Supports ongoing standard deviation and mean calculations for stream-based datasets.

Required Python Modules
=======================

* numpy
* pytest


Developers
===========

* Nathaniel Burbank
* Rohan Thavarajah
* Nicholas Ruta
* Jonne Saleva


Note
====

This project has been set up using PyScaffold 2.5.7. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.
