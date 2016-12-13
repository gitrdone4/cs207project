# handy_helpers.py
# (c) Jonne Saleva, Nathaniel Burbank, Rohan Tharavajah, Nicholas Ruta

# description:
# functions that do all kinds of
# stuff that you don't want to
# implement over and over again

def bisect_tuples(list_of_tuples):
    """
    Description
    -----------
    Takes in a list of tuples,
    processes it, and returns two
    lists, called `first_elems`, and
    `second_elems`

    Parameters
    ----------
    list_of_tuples: sequence of tuples

    Returns
    -------
    out: list of lists
        nested list that contains
        lists of first and second
        elements, respectively.

    Example
    -------
    >>> arr = [(1,2), (3,4), (5,6)]
    >>> odds, evens = bisect_tuples(arr)
    >>> odds == [1,3,5]
    True
    >>> evens == [2,4,6]
    True
    """

    out = [[t[j] for t in list_of_tuples]
                 for j in (0, 1)]

    return out

