# helper_functions.py
# functions to make certain flask tasks easier.
# (c) Jonne Saleva, Nathaniel Burbank, Nicholas Ruta, Rohan Thavarajah

from flask import render_template, make_response, jsonify, request

def parse_timeseries_get(arg_name, arg_val):
    """
    Description
    ----------
    Parses query argument strings by splitting along
    the appropriate separator character, and
    returns a sequence of (a) bounds [in the case
    of `mean_in`] or (b) acceptable values [in the
    case of `level_in`]

    Parameters
    ----------
    arg_name: str
        query string of the form '?level_in=A,B,C'.
        comes after the URL in the web browser.

    arg_val: str
        name of the argument we are trying to filter.
        can be `mean_in` or `level_in`.`

    Returns
    -------
    correct bounds / values for the query string parameters.
    """

    # initialize separator lookup dict
    separators = {
        'mean_in': '-', 
        'level_in': ',', 
        'level': ','
    }

    # validate `arg_name` input
    if arg_name not in separators:
        raise 

    # get the right separtor, split and return
    sep = separators[arg_name]
    return tuple(arg_val.split(sep))

def get_filter_expression(query_args):
    """
    Description
    -----------
    Parses the query arguments of an HTTP GET request
    to our Flask app, and constructs a filter 
    expression (string of SQL) to be used in querying 
    the PostgreSQL metadata DB.

    Parameters
    ----------
    None.

    Returns
    -------
    A list of SQL filter expessions as strings
    """

    def _create_sql_filter(arg):

        # first parse the actual string argument
        arg_vals = parse_timeseries_get(arg, query_args[arg])

        if arg == "level_in":
            filter_exp = "ts_metadata_level IN {}".format(arg_vals)

        elif arg == "mean_in":
            filter_exp = "ts_metadata_mean >= {} AND ts_metadata_mean <= {}"\
                            .format(*arg_vals)

        elif arg == "level":
            filter_exp = "ts_metadata_level = '{}'".format(*arg_vals)

        # append final result to filters list
        return filter_exp

    filter_string = ' AND '.join([_create_sql_filter(arg) for arg in query_args])

    return filter_string
