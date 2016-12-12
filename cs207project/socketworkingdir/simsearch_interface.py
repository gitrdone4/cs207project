import cs207project.tsrbtreedb.simsearch
from cs207project.storagemanager.filestoragemanager import FileStorageManager
from cs207project.tsrbtreedb.makelcs import clear_dir
from cs207project.tsrbtreedb.genvpdbs import create_vpdbs
from cs207project.tsrbtreedb.settings import LIGHT_CURVES_DIR, DB_DIR, TS_LENGTH, tsid_to_fn

def

def simsearch_by_id(id,n=5):
	"""
	Args:
		id: int id of existing ts in database (e.g (547))
		n: number of time series to return. (Defaults to 5)

	Returns:
		Returns a dictionary of the n closest time series ids keyed by distances
		{.456:"ts_425", .3021:"ts_537"}

	Raises:
		ValueError: If id does not exist in the database

	"""
	fsm = FileStorageManager(LIGHT_CURVES_DIR)
	input_ts = simsearch.load_ts(tsid_to_fn(id),fsm):
	closest_vp = simsearch.find_closest_vp(load_vp_lcs(DB_DIR,LIGHT_CURVES_DIR), input_ts)

	return simsearch.search_vpdb_for_n(closest_vp,input_ts,db_dir,lc_dir,n)


def simsearch_by_ts(ts,n=5):
	"""
	Args:
		ts: a (JSON???) encapsulation of an external time series;
			(Although it would be easier if you sent an array time series object)
		n: number of time series to return. (Defaults to 5)

    Returns:
    	Returns a three argument tuple:
		 - First element is a dictionary of the n closest time series ids keyed by
		distances.
		 - Second augment is the newly assigned id of the new time series (if it's new) or
		 the id of the existing ts if it's not new.
		 - Third element is a bool to report whether the ts is new or not.

		Example: ({.456:"ts_425",.3021:"ts_537"},1201,True)

	Notes:

		Third augment is a boolean value that's True if the the submitted ts is "new /non-existent"
		time series, false if it already exists. We test for already exists by
		checking if there's a time series in the database with a distance of 0 (or
		very close to zero)

	"""
	is_new = False
	fsm = FileStorageManager(LIGHT_CURVES_DIR)
	interpolated_ats = ts.interpolate(np.arange(0.0, 1.0, (1.0 /TS_LENGTH)))
	closest_vp = simsearch.find_closest_vp(load_vp_lcs(DB_DIR,LIGHT_CURVES_DIR),interpolated_ats)
	n_closest_dict, tsid = search_vpdb_for_n(closest_vp,input_ts,db_dir,lc_dir,n)

	if tsid == -1:
		is_new = True
		tsid = fsm.get_unique_id()
    	fsm.store(unique_id, tsid)

    return (n_closest_dict,tsid,is_new)


def rebuild_vp_indexs():
	"""
	Rebuilds vantage point "databases" based on time series that have been
	saved to disk. May take some time(up to 30 seconds in my experience)
	should be called after simsearch_by_ts if simsearch_by_ts returns True and
	has added a new time series to disk.

	"""
	simsearch.create_vpdbs(20,LIGHT_CURVES_DIR,DB_DIR)

def get_by_id(id):
	"""
	Args:
		id: int id of existing ts in database (e.g (547))

	Returns:
		Returns the array time series object associated with id

	Raises:
		ValueError: If id does not exist in the database

	"""
	fsm = FileStorageManager(LIGHT_CURVES_DIR)
	try:
		ats = simsearch.load_ts(tsid_to_fn(id),fsm)
		return ats
	except ValueError:
		raise #Can not find ts by that id


