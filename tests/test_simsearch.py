#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import numpy as np
import random

from pytest import raises

from cs207project.tsrbtreedb.crosscorr import kernel_corr, kernel_dist, standardize, ccor
import cs207project.tsrbtreedb.makelcs as makelcs
from cs207project.tsrbtreedb.makelcs import clear_dir, tsmaker, random_ts
import cs207project.tsrbtreedb.genvpdbs as genvpdbs
import cs207project.tsrbtreedb.simsearch as simsearch
import cs207project.tsrbtreedb.simsearchutil as simsearchutil
from cs207project.storagemanager.filestoragemanager import FileStorageManager
import cs207project.tsrbtreedb.unbalancedDB as unbalancedDB


from cs207project.tsrbtreedb.settings import TEMP_DIR, LIGHT_CURVES_DIR, DB_DIR, SAMPLE_DIR

def test_value_and_file_asserts():
    """Confirm that we raise value error when attempting to load non-existent time series """
    lc_temp_dir = TEMP_DIR + LIGHT_CURVES_DIR
    fp = "Non-existent file path"
    with raises(IOError):
        simsearch.load_nparray(fp)

    with raises(ValueError):
        simsearch.load_ts(fp,FileStorageManager(lc_temp_dir))

def test_makelcs():
    lc_temp_dir = TEMP_DIR + LIGHT_CURVES_DIR
    db_temp_dir = TEMP_DIR + DB_DIR

    # Before we've generated anything, confirm that our rebuild detector method properly detects that we need to rebuild
    assert(simsearch.need_to_rebuild(lc_temp_dir,db_temp_dir) == True)

    makelcs.make_lcs_wfm(5,lc_temp_dir)
    assert(simsearch.need_to_rebuild(lc_temp_dir,db_temp_dir) == True)

    clear_dir(TEMP_DIR,recreate=False)
    # Generate 100 light curves in temp dir
    makelcs.make_lcs_wfm(100,lc_temp_dir)
    assert(simsearch.need_to_rebuild(lc_temp_dir,db_temp_dir) == True)

    # load that back in from disk
    lc_dict = genvpdbs.load_ts_fsm(lc_temp_dir)
    assert(len(lc_dict) == 100)


def test_genvpdbs():
    lc_temp_dir = TEMP_DIR + LIGHT_CURVES_DIR
    db_temp_dir = TEMP_DIR + DB_DIR

    # Create 10 vantage point database files
    genvpdbs.create_vpdbs(10,lc_temp_dir,db_temp_dir)

    # With vantage points created, we should have fully created dataset
    assert(simsearch.need_to_rebuild(lc_temp_dir,db_temp_dir) == False)

    # Load vantage points back in from disk
    vp_dict = simsearch.load_vp_lcs(db_temp_dir,lc_temp_dir)
    assert(len(vp_dict) == 10)

    clear_dir(TEMP_DIR,recreate=False)


def test_simsearch():
    lc_temp_dir = TEMP_DIR + LIGHT_CURVES_DIR
    db_temp_dir = TEMP_DIR + DB_DIR

    simsearch.rebuild_lcs_dbs(lc_temp_dir,db_temp_dir,10,100)

    # Repeat checks from above on re-generated data
    lc_dict = genvpdbs.load_ts_fsm(lc_temp_dir)
    assert(len(lc_dict) == 100)
    vp_dict = simsearch.load_vp_lcs(db_temp_dir,lc_temp_dir)
    assert(len(vp_dict) == 10)
    assert(simsearch.need_to_rebuild(lc_temp_dir,db_temp_dir) == False)

    demo_ts_fn = random.choice(os.listdir('cs207project/tsrbtreedb/' + SAMPLE_DIR))
    demo_fp = 'cs207project/tsrbtreedb/' + SAMPLE_DIR + demo_ts_fn
    simsearchutil.sim_search(demo_fp,db_temp_dir,lc_temp_dir,False)

def test_crosscorr():

    t1 = standardize(tsmaker(0.5, 0.1, random.uniform(0,10)))

    # First confirm that the kernel correlation and distance methods
    # return 1 and 0 when comparing a ts with itself
    assert(kernel_corr(t1,t1) == 1)
    assert(kernel_dist(t1,t1) == 0)

    t2 = standardize(tsmaker(0.5, 0.1, random.uniform(0,10)))
    t3 = standardize(random_ts(0.5))

    # Now let's do the opposite -- ensure that we see some distance for different curves
    assert(kernel_dist(t1,t2) > 0)
    assert(kernel_dist(t1,t3) > 0)
    assert(kernel_corr(t1,t2) < 1)
    assert(kernel_corr(t1,t3) < 1)

def test_crosscorr_errors():
    """Test that we have checks for varies error conditions"""

    t1 = standardize(tsmaker(0.5, 0.1, random.uniform(0,10)))
    t4 = standardize(random_ts(0.5,200))
    t5 = tsmaker(0.5, 0.1, random.uniform(0,10))

    #Confirm that we raise value error if we attempt to compare time series
    # that are not the same length
    with raises(ValueError):
        ccor(t1, t4)

    with raises(ValueError):
        kernel_dist(t1, t4)

    with raises(ValueError):
        kernel_corr(t1,t4)

    #Confirm that we raise value error if we attempt to compare time series
    # that have not been standardized first
    t5 = tsmaker(0.5, 0.1, random.uniform(0,10))
    with raises(ValueError):
        kernel_dist(t4, t5)


## Tests for unbalanced binary tree (Was created for part 7, but it no longer used)

def test_db_1():
    db_fname = TEMP_DIR + "test1.dbdb"
    db = unbalancedDB.connect(db_fname)
    assert os.path.isfile(db_fname) == True
    db.close()

    db = unbalancedDB.connect(db_fname)
    db.set(16, "big")
    db.set(15, "med")
    db.set(14, "sml")
    db.commit()
    db.close()

    db = unbalancedDB.connect(db_fname)
    assert db.get(16)=='big' # test get()
    assert db.get_min()=='sml' # test get_min()
    assert db.get_left(16)==(15, u'med') # test get_left()
    assert db.get_left(15)==(14, u'sml') # so the tree is indeed unbalanced
    assert db.chop(15.5)==[(15, u'med'), (14, u'sml')] # test chop is robust to whether the tree is balanced or not
    db.close()

    db = unbalancedDB.connect(db_fname)
    db.set(16, "really big")
    db.close()

    db = unbalancedDB.connect(db_fname)
    assert db.get(16)=='big' # test commit required for changes to be finalized
    db.close()

def test_db_2():
    # a more complicated balanced example
    db_fname = TEMP_DIR + "test2.dbdb"
    db = unbalancedDB.connect(db_fname)
    assert os.path.isfile(db_fname) == True
    db.close()

    db = unbalancedDB.connect(db_fname)
    input_data = [
        (8,"eight"),
        (3,"three"),
        (10,"ten"),
        (1,"one"),
        (6,"six"),
        (14,"fourteen"),
        (4,"four"),
        (7,"seven"),
        (13,"thirteen"),
        ]
    for key, val in input_data:
        db.set(key, val)
    db.commit()
    db.close()

    db = unbalancedDB.connect(db_fname)
    # testing
    assert db.get_left(8)==(3,"three")
    assert db.get_right(8)==(10,"ten")
    assert db.get_left(3)==(1,"one")
    assert db.get_right(3)==(6,"six")
    assert db.get_left(6)==(4,"four")
    assert db.get_right(6)==(7,"seven")
    assert db.get_right(10)==(14,"fourteen")
    assert db.get_left(14)==(13,"thirteen") # ensure that we do match wikipedia
    assert db.chop(6)==[(3, u'three'), (1, u'one'), (6, u'six'), (4, u'four')] # test chop on key in database
    assert db.chop(6.1)==[(3, u'three'), (1, u'one'), (6, u'six'), (4, u'four')] # test chop on key out of database
    db.close()

def test_clear():
    """Clear test dir for tests"""
    clear_dir(TEMP_DIR,recreate=False)

