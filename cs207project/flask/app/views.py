# views.py
# (c) Jonne Saleva, Nathaniel Burbank, Nicholas Ruta, Rohan Thavarajah

# Description:
# RESTful api for CS 207 Final Project. Designed to interface
# with the PostgreSQL metadata database, the Storage Manager,
# and the socket-fronted Red-Black Tree database

from flask import make_response, jsonify, request, url_for, render_templa
from cs207project.timeseries import arraytimeseries as arrts
import cs207project.socketclient.client as cl
from cs207project.handy_helpers import *
from cs207project.flask.app import app, db, models
from cs207project.flask.helper_functions import *
import json

# ARGUMENT VALIDATION
def validate(args, route, request_type):
    """
    Description
    -----------
    Validates query string or JSON payload
    depending on the route and request type.

    Parameters
    ----------
    args: dict-like
        key-value pairs for query string arguments.
        alternatively json payload as dict

    route: str
        route we are trying to access.
        e.g. '/timeseries/'

    request_type: str
        type of request we are trying to perform.
        must be 'GET' or 'POST'
    """

    valid_json_fields = ['id','time', 'value']

    if route == '/timeseries':

        if request_type == 'GET':
            pass

        elif request_type == 'POST':
            pass

    elif route == '/timeseries/id':
        pass

    elif route == '/simquery':

        if request_type == 'GET':
            pass

        elif request_type == 'POST':
            pass

# API ENDPOINTS
@app.route('/')
def front_page():
    """
    Renders instructions in case the user tried
    to access the "front page" of the API
    """

    return render_template('index.html')

@app.route('/timeseries/', methods=['GET', 'POST'])
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
    Takes JSON as input, adds it to time series DB
    and returns it as JSON. Note that the id is generated
    by our simsearch database, and not the user, so as to
    avoid error handling with already existing ids.

    Returns
    -------
    HTTP Response with requested time series (meta)data.
    """

    # GET request
    if request.method == 'GET':

        # parse query string and create filter expressions
        filter_string = get_filter_expression(request.args)

        # filter and execute query
        metadata = fetch_metadata(filter_string)

        # create response from query result, jsonify and return
        response = [ts.to_dict() for ts in metadata]

    elif request.method == 'POST':

        # step 1: get json, decode with ascii and make a dict
        response_txt = request.data.decode('ascii')
        response = json.loads(response_txt)

        # step 2: json to arraytimeseries
        new_ts = arrts.ArrayTimeSeries.from_dict(response)

        # step 3: add timeseries to db
        new_tsid = cl.save_ts_to_db(new_ts)

        # step 4: return the timeseries 
        # (no need for new request, can do locally)
        return cl.get_ts_with_id(new_tsid)

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

    Response is of the format:
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
    except:
        return not_found('Time series with id {} not found in DB!'.format(tsid))

    # get metadata
    metadata = fetch_metadata('ts_metadata_id = {}'.format(tsid))

    # create response from query result, jsonify and return
    response = {
                'id': tsid,
                'metadata': [ts.to_dict() for ts in metadata],
                'time_series': actual_ts.to_dict()
            }

    return make_response(jsonify(response), 200)

@app.route('/simquery/', methods=['GET', 'POST'])
def get_similar():
    """
    Description
    ------------

    GET
    ---
    Fetches IDs for five most similar time series
    for the one specified by `tsid`.

    POST
    ----
    Fetches IDs for five most similar time series
    for the one specified in the JSON payload   

    Parameters
    ----------
    GET
    ---
    tsid: int

    POST
    ----
    payload: json

    Returns
    -------
    JSON of IDs of the five time series closest to
    the one specified by `tsid`.
    """

    if request.method == 'GET':

        # get ts id from query string
        tsid = int(request.args['the_id'])

        # get nearest
        vptdb_output = cl.get_n_nearest_ts_for_tsid(tsid)
        nn_dist, nn_ids = bisect_tuples(vptdb_output.items())
        response = [
            {
                'id': int(idx),
                'distance': float(dist)
            } for idx, dist in zip(nn_ids, nn_dist)
        ]

        return make_response(jsonify(response), 200)

    elif request.method == 'POST':
        pass    


# API ERROR HANDLING
@app.errorhandler(404)
def not_found(err):
    """
    Blanket HTTP Error Code 404
    """
    response = {
        'error_code': 404,
        'error_message': str(err)
    }
    
    return make_response(jsonify(response), 404)

@app.errorhandler(400)
def bad_request(err):
    """
    Blanket HTTP Error Code 400
    """
    response = {
        'error_code': 400,
        'error_message': str(err)
    }
    return make_response(jsonify(response), 400)
