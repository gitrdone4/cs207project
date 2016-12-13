# test_flask.py
# (c) Jonne Saleva, Nathaniel Burbank, Nicholas Ruta, Rohan Thavarajah

# description:
# unit tests for flask interface.

# imports
from flask import render_template, make_response, jsonify, request
from cs207project.flask.helper_functions import *
from cs207project.flask.app import app, db, models
import flask_restful
import re

# test suite
"""
Tests that should be run:
- basic endpoint connectivity: 
	- /timeseries/ works and returns metadata
	- /timeseries/level_in returns subset of levels
	- /timeseries/level_in fails gracefully if given nonexistent level (incl composite case)
	- /timeseries/level_in fails gracefully if given no input (invalid url string)
"""