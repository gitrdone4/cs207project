# views.py
# (c) Jonne Saleva, Nathaniel Burbank, Nicholas Ruta, Rohan Thavarajah

# Description:
# RESTful api for CS 207 Final Project. Designed to interface
# with the PostgreSQL metadata database, the Storage Manager,
# and the socket-fronted Red-Black Tree database

from flask import render_template, make_response, jsonify, request
from flask_restful import reqparse
from helper_functions import *
from app import app, db, models
import re

# index
@app.route('/')
def render_index():
	return make_response('Hello World!')

@app.route('/timeseries/', methods=['GET'])
def get_metadata():
    """
    Fetches metadtata on all the time series.
    """

    # GET request
    if request.method == 'GET':
        
        # grab query string
        query_string = request.args

        # iterate over arguments in query,
        # string and parse them as needed.
        filters = []
        for arg in query_string:
            
            # first parse the actual string argument
            arg_vals = parse_query_string(arg, query_string[arg])
            
            if arg == 'level_in':
                filter_exp = 'ts_metadata_level IN {}'.format(arg_vals)
            
            elif arg == 'mean_in':
                filter_string = 'ts_metadata_mean >= {} AND ts_metadata_mean <= {}'\
                                .format(*arg_vals)

            elif arg == 'id':
                pass # TODO
            
            # append final result to filters list
            filters.append(filter_string)

        # concatenate individual
        filter_string = ' AND '.join(filters)

        # filter and execute query
        query = models.TSMetadata\
                            .query\
                            .filter(filter_string)\
                            .all()

        # create response from query result, jsonify and return
        response = [{'id': ts.id, 'mean': ts.mean, 'std': ts.std,
                    'blarg': ts.blarg, 'level': ts.level} for ts in query]

        return make_response(jsonify(response))

    # POST request
    else:
        pass

@app.route('/timeseries/', methods=['POST'])
def add_ts_and_fetch():
	"""
	Adds TS to database and fetches it afterwards.
	"""
	pass

@app.route('/simquery', methods=['GET', 'POST'])
def blargh():
    pass