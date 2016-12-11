import cs207project.tsrbtreedb.simsearch
from cs207project.storagemanager.filestoragemanager import FileStorageManager
from cs207project.tsrbtreedb.settings import LIGHT_CURVES_DIR, DB_DIR, TS_LENGTH


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
	pass

def simsearch_by_ts(ts,n=5):
		"""
	Args:
		ts: a (JSON???) encapsulation of an external time series;
			(Although it would be easier if you sent an array time series object)
		n: number of time series to return. (Defaults to 5)

    Returns:
    	Returns a three argument tuple: (closest_dist_dic,new_bool,id).
		First argument is a dictionary of the n closest time series ids keyed by
		distances. Second augment is the newly assigned id of the new time series (if
		it does not exist) or the id of the existing ts. if we find a match.

		Example: ({.456:"ts_425",.3021:"ts_537"},1201,True)

	Notes:

		Third augment is a boolean value that's True if the the submitted ts is "new /non-existent"
		time series, false if it already exists. We test for already exists by
		checking if there's a time series in the database with a distance of 0 (or
		very close to zero)

	"""
	pass

def rebuild_vp_indexs():
	"""
	Rebuilds vantage point "databases" based on time series that have been
	saved to disk. May take some time(up to 30 seconds in my experience)
	should be called after simsearch_by_ts if simsearch_by_ts returns True and
	has added a new time series to disk.

	"""
	pass