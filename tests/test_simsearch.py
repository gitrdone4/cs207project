#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# CS207 Group Project Part 7
# Created by Team 2 (Jonne Seleva, Nathaniel Burbank, Nicholas Ruta, Rohan Thavarajah) for Team 4

import sys
import os
import numpy as np
import random

import cs207project.tsrbtreedb.crosscorr as cross
import cs207project.tsrbtreedb.makelcs as makelcs
from cs207project.tsrbtreedb.makelcs import clear_dir
import cs207project.tsrbtreedb.genvpdbs as genvpdbs
import cs207project.tsrbtreedb.simsearch as simsearch
import cs207project.tsrbtreedb.unbalancedDB as unbalancedDB
import cs207project.timeseries
from cs207project.tsrbtreedb.settings import TEMP_DIR, LIGHT_CURVES_DIR, DB_DIR

def test_makelcs():
    lc_temp_dir = TEMP_DIR + LIGHT_CURVES_DIR
    db_temp_dir = TEMP_DIR + DB_DIR

    assert(simsearch.need_to_rebuild(lc_temp_dir,db_temp_dir) == True)


    makelcs.make_lc_files(100,lc_temp_dir)
    assert(simsearch.need_to_rebuild(lc_temp_dir,db_temp_dir) == True)
    ts = genvpdbs.load_ts(lc_temp_dir)
    assert(len(ts) == 100)

    genvpdbs.create_vpdbs(10,lc_temp_dir,db_temp_dir)
    assert(simsearch.need_to_rebuild(lc_temp_dir,db_temp_dir) == False)


def test_simsearch():
    lc_temp_dir = TEMP_DIR + LIGHT_CURVES_DIR
    db_temp_dir = TEMP_DIR + DB_DIR

    gen_lc_fns = []
    for file in os.listdir(lc_temp_dir):
        if file.startswith("ts-") and file.endswith(".txt"):
            gen_lc_fns.append(file)

    lc_fn = random.sample(gen_lc_fns, 1)

    lc_path = lc_temp_dir + lc_fn[0]

    simsearch.sim_search(lc_path,db_temp_dir,lc_temp_dir,plot=False)


    #clear_dir(TEMP_DIR,recreate=False)

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
    clear_dir(TEMP_DIR,recreate=False)

def test_ccorr():
    from cs207project.tsrbtreedb.makelcs import tsmaker
    from cs207project.tsrbtreedb.crosscorr import kernel_corr, kernel_dist, standardize
    t1 = standardize(tsmaker(0.5, 0.1, random.uniform(0,10)))
    t2 = standardize(tsmaker(0.5, 0.1, random.uniform(0,10)))
    assert(kernel_corr(t1,t1) == 1)
    assert(kernel_dist(t1,t1) == 0)


