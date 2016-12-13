# views.py
# (c) Jonne Saleva, Nathaniel Burbank, Nicholas Ruta, Rohan Thavarajah

# Description:
# RESTful api for CS 207 Final Project. Designed to interface
# with the PostgreSQL metadata database, the Storage Manager,
# and the socket-fronted Red-Black Tree database

from flask import make_response, jsonify, request, url_for
from cs207project.timeseries import arraytimeseries
import cs207project.socketclient.client as cl
from app import app, db, models
from helper_functions import *
from flask_api import status

# API ENDPOINTS
@app.route('/')
def render_index():
    return make_response(
            jsonify({'message': 'Select an endpoint!'}), 400
        )

@app.route('/timeseries/', methods=['GET'])
def get_metadata():
    """
    Description
    -----------
    Handles GET and POST requests for API endpoint /timeseries/.

    Parameters
    ----------
    
    Case 1: GET (query string parameters)
    ------------
    mean_in: string
        string of format 'lower-upper',
        specifying lower and upper bounds
    level_in: string
        comma-separated sequence indicating
        levels for which to fetch time series
        metadata. must be one of A, B, ..., F.
    level: string
        single level in case a range is too much.
        must be one of A, B, ..., F. 

    Case 2: POST
    ------------
    Takes JSON as input
    
    Returns
    -------
    HTTP Response with requested time series (meta)data.
    """

    # GET request
    if request.method == 'GET':

        # parse query string and create filter expressions
        filter_string = get_filter_expression(request.args)

        # filter and execute query
        metadata = models.TSMetadata\
                    .query\
                    .filter(filter_string)\
                    .all()

        # create response from query result, jsonify and return
        response = [ts.to_dict() for ts in metadata]
    
    elif request.method == 'POST':

        pass

    return make_response(jsonify(response), 200)

@app.route('/timeseries/<int:tsid>', methods=['GET'])
def get_ts_and_metadata(tsid=None):
    """
    Description
    -----------
    Handles GET requests for API endpoint /timeseries/id.

    Fetches both time series itself (through socket) 
    and metadata (from PostgreSQL) for the tsid.

    Parameters
    ----------
    tsid: int
        id of the desired time series

    Returns
    -------
    HTTP Response with requested time series (meta)data.

    Reponse is of the format:
    {
        'id': tsid,
        'metadata': {...}
        'time_series_data': [
            'time': [...],
            'value': [...]
        ]
    }
    """

    # get actual ts from socket
    try:
        actual_ts = cl.get_ts_with_id(tsid)
    except Exception as e:
        return not_found(e)

    # get metadata
    metadata = models.TSMetadata\
                .query\
                .filter(models.TSMetadata.id == tsid)

    # create response from query result, jsonify and return
    response = {
                'id': tsid,
                'metadata': [ts.to_dict() for ts in metadata],
                'time_series': actual_ts.to_dict()
            }

    return make_response(jsonify(response), 200)

@app.route('/timeseries/', methods=['POST'])
def add_ts_and_fetch():
    pass

@app.route('/simquery', methods=['GET', 'POST'])
def blargh():
    pass


# API ERROR HANDLING
@app.errorhandler(404)
def not_found(err):
    """
    Blanket HTTP Error Code 404
    """
    resp = {
        'error_code': 404,
        'message': str(err)
    }
    return make_response(resp), 404

@app.errorhandler(400)
def bad_request(err):
    """
    Blanket HTTP Error Code 400
    """
    resp = {
        'error_code': 400,
        'message': err
    }
    return make_response(jsonify(resp), 400)