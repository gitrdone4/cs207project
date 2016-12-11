# helper_functions.py
# functions to make certain flask tasks easier.
# (c) Jonne Saleva, Nathaniel Burbank, Nicholas Ruta, Rohan Thavarajah

def parse_query_string(arg_name, arg_val):
    """
    Description
    ----------
    Parses query string by splitting along
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
    separators = {'mean_in': '-', 'level_in': ',', 'id': ','}

    # validate `arg_name` input
    assert arg_name in separators

    # get the right separtor, split and return
    sep = separators[arg_name]
    return tuple(arg_val.split(sep))
