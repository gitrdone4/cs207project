# views.py
# (c) Jonne Saleva, Nathaniel Burbank, Nicholas Ruta, Rohan Thavarajah

# Description:
# RESTful api for CS 207 Final Project. Designed to interface
# with the PostgreSQL metadata database, the Storage Manager,
# and the socket-fronted Red-Black Tree database

from flask import render_template, make_response, jsonify, request
from app import app, db, models

# index
@app.route('/')
def render_index():
	return make_response('Hello World!')

@app.route('/timeseries/', methods=['GET'])
def get_metadata():
    """
	Fetches metadtata on all the time series.
	"""
    query = models.TSMetadata.query.all()
    response = [{'id': ts.id, 'mean': ts.mean, 'std': ts.std,
                'blarg': ts.blarg, 'level': ts.level} for ts in query]
    return make_response(jsonify(response))

@app.route('/timeseries/', methods=['POST'])
def add_ts_and_fetch():
	"""
	Adds TS to database and fetches it afterwards.
	"""
	pass
