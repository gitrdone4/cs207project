# test_flask.py
# (c) Jonne Saleva, Nathaniel Burbank, Nicholas Ruta, Rohan Thavarajah

# description:
# unit tests for flask interface.

# imports
# from flask import render_template, make_response, jsonify, request
# from cs207project.flask.helper_functions import *
# from cs207project.flask.app import app, db, models

# test suite
"""
Tests that should be run:
- basic endpoint connectivity:
	- /timeseries/ GET
		- /timeseries/ works and returns metadata
		- /timeseries/level_in returns subset of levels
		- /timeseries/level_in returns subset of levels
		- /timeseries/level_in if given nonexistent level (incl composite case)
		- /timeseries/level_in if given no input (invalid url string)
		- /timeseries/level_in: non-letter inputs, wrong separator
		- /timeseries/mean_in: non-numeric inputs, wrong separator
		- /timeseries/mean_in: input not in sorted order
	- /timeseries/ POST

-
"""
