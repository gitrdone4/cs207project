
import os
import random
import threading
import collections
import time
from pytest import raises

from cs207project.tsrbtreedb.settings import LIGHT_CURVES_DIR, DB_DIR, TS_LENGTH, SAMPLE_DIR, TEMP_DIR
from cs207project.tsrbtreedb.makelcs import clear_dir, tsmaker, random_ts
from cs207project.tsrbtreedb.simsearch_interface import simsearch_by_id,rebuild_if_needed, get_by_id,add_ts,simsearch_by_ts
from cs207project.tsrbtreedb.crosscorr import kernel_corr, kernel_dist, standardize, ccor

from cs207project.socketclient.serialization import serialize, Deserializer
from socketserver import BaseRequestHandler, TCPServer,ThreadingTCPServer
from cs207project.tsrbtreedb.socket_server import EchoHandler
from cs207project.socketclient import client as s_client

def test_setup_temp_dir():
    """Clear existing temp dir and change working dir to be inside it"""
    clear_dir(TEMP_DIR)
    os.chdir(TEMP_DIR)


def test_rebuild_if_needed():
    # Make small db with 250 light curves
    rebuild_if_needed(LIGHT_CURVES_DIR,DB_DIR,n_vps=10,n_lcs=250)

    # Attempt to get non-existent time series
    with raises(ValueError):
        n_closest = simsearch_by_id(500,3)

    with raises(ValueError):
        _ = get_by_id(500)

def test_n_closest():
    """
    Get ts 100; run search by id in on, confirm we get back 3 close ts
    and that distances in returned dict match actual distances
    """
    # Get ts 100
    ats_100 = get_by_id(100)

    n_closest = simsearch_by_id(100,3)
    assert(len(n_closest) == 3)

    # Confirm that distance measures are accurate
    for dist in n_closest:
        tsid = n_closest[dist]
        other_ts = get_by_id(tsid)
        assert(abs(dist - kernel_dist(standardize(ats_100), standardize(other_ts)) < .0001))

def test_simsearch_by_ts():
    ats_75 = get_by_id(75)
    n_closest_dict,tsid,is_new = simsearch_by_ts(ats_75,5)
    assert(tsid == 75)
    assert(is_new == False)
    assert(n_closest_dict == simsearch_by_id(75,5))

    new_ts = standardize(tsmaker(0.5, 0.1, random.uniform(0,10)))
    n_closest_dict,tsid,is_new = simsearch_by_ts(new_ts,5)
    assert(is_new == True)
    assert(tsid > 250)
    assert(len(n_closest_dict) == 5)

def test_add_ts():
    """ Create a ts, add to db, retrieve it, assert that it's the same ts"""
    new_ts = standardize(tsmaker(0.5, 0.1, random.uniform(0,10)))

    new_tsid = add_ts(new_ts)
    ts_as_saved = get_by_id(new_tsid)
    assert(kernel_dist(standardize(ts_as_saved), standardize(new_ts)) < .00001)

    # Confirm that we get the same id back when we attempt to add it a second time

    assert(add_ts(new_ts) == new_tsid)

def test_socket_server():
    # startup server on separate thread
    global serv
    serv = ThreadingTCPServer(('', 20001), EchoHandler)
    server_thread = threading.Thread(target=serv.serve_forever)
    server_thread.start()

def test_get_by_id_over_socket():
    """Name says it all """
    ats100 = get_by_id(100)
    assert(ats100 == s_client.get_ts_with_id(100))

def test_get_n_nearest_ts_for_tsid():
    """ Request closest ts by id over socket; compare results to (non socket) simsearch_by_id method """
    s_n_closest_dict = s_client.get_n_nearest_ts_for_tsid(99,5)
    n_closest_dict = simsearch_by_id(99,5)
    for tsid in s_n_closest_dict.values():
        assert(tsid in n_closest_dict.values())

def test_get_n_nearest_ts_for_ts():
    """
    Make new ts. Send over socket, and request nearest ts.
    Compare results to (non socket) simsearch_by_id method
    """
    new_ts = tsmaker(0.5, 0.1, random.uniform(0,10))
    d = s_client.get_n_nearest_ts_for_ts(new_ts,5)
    s_n_closest_dict = d['n_closest_dict']
    n_closest_dict = simsearch_by_id(d['tsid'],5)
    for tsid in s_n_closest_dict.values():
        assert(tsid in n_closest_dict.values())

def test_save_ts_to_db():
    # Save a ts, request it by id, compare to original
    new_ts = (tsmaker(0.5, 0.1, random.uniform(0,10)))
    new_tsid = s_client.save_ts_to_db(new_ts)
    echo_ts = s_client.get_ts_with_id(new_tsid)
    assert(kernel_dist(standardize(echo_ts), standardize(new_ts)) < .00001)

def test_shutdown_socket_server():
    """Shutdown socket server"""
    serv.shutdown()

def test_clear_temp_dir():
    """ Clears temp dir"""
    os.chdir(os.pardir)
    clear_dir(TEMP_DIR,recreate=False)

