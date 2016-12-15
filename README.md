# GitRdone4 Time Series

A flexible collection of python classes for searching and analyzing time series data.

[![Build Status](https://travis-ci.org/gitrdone4/cs207project.svg?branch=master)](https://travis-ci.org/gitrdone4/cs207project)

[![Coverage Status](https://coveralls.io/repos/github/gitrdone4/cs207project/badge.svg?branch=master)](https://coveralls.io/github/gitrdone4/cs207project?branch=master)

Final group project for Harvard's CS 207 course, [Systems Development for Computational Science](https://iacs-cs207.github.io/cs207-2016/) (Fall 2016).

### Overview

Time series are two-dimensional (or higher) arrays of numeric data, where ordered time-values are bound to specific data points that represent specific outcomes, measurements, or other values associated with specific times.  While time series data can be stored using traditional arrays or tables, the classes included in this library make working with these types of data sets in python easier by enforcing the core properties of a time series at a class level. For example, in a time series no two times can be repeated. And every represented value needs a time associated with it. By creating and manipulating data-sets using these classes, these properties are enforced at all times.

The UI that we have provided displays one larger primary chart of the id in question. Additionally, it provides 5 charts that compare the most similar time series, provided by the /simquery rest endpoint, and allows for each one to become the primary chart on the page.

### Instructions for Running the Project in an EC2 Instance
1. Create an Ubuntu 16.04 instance on Amazon EC2.
2. During instance creation, select the security group option to allow HTTP access on port 80.
3. Connect via ssh:
```
$ chmod 0400 pair.sem
$ sudo ssh -i "pair.pem" ubuntu@insert_public_ip
```
4. Run the following commands to provision the system:
```
git clone https://github.com/gitrdone4/cs207project.git

cd ~/cs207project/conf

bash cs207_bash.sh
press q when nginx server pauses runtime with message stating that the process has started

bash serversetup.sh

You should now be able to hit the home page in a browser!

If you would like to see the site in a previously set up instance, visit http://54.175.17.217/

To test the file upload for a time series, upload the file cs207project/file_upload_ts.js
```

### How to install our cs207project libraries
1. Clone repo
2. Run `python setup.py install` from the root directory 'cs207project'

### Running tests

Just run `python setup.py test`

### Internal Modules

- Timeseries: class implementations for TimeSeries,Array Time Series, and  Stream Time Series
- RBTree: RedBlack Tree database for saving sorted key-value pairs to disk
- Storagemanager: Class for managing ids and storing time series to disk
- tsrbtreedb: Module for searching through time series based on similarity. Provides a command line and socket server interface for performing similarity searches.
- socketclient: Socket Client for sending and retrieving time series data over a network connection from simsearch socket server.

### Additional Time Series Class Features

1. Supports adding, subtracting, multiplying, and other manipulations on fixed-length data sets.
2. Support manipulation of time-series streams (i.e., data sets that are ongoing, and don't have fixed storage)
3. Supports piecewise linear interpolation of non-existing values within the domain of existing fixed-length data-sets.
4. Supports ongoing standard deviation and mean calculations for  stream-based datasets.

### Required Python Modules

- [NumPy](http://www.numpy.org)
- [Pytest](http://doc.pytest.org/en/latest/)
- [Flask](http://flask.pocoo.org)
- [Flask-sqlalchemy](Flask-sqlalchemy)
- [Portalocker](https://pypi.python.org/pypi/portalocker)
- [SciPy](https://www.scipy.org)

### Developers:
- Jonne Saleva
- Nathaniel Burbank
- Nicholas Ruta
- Rohan Thavarajah
