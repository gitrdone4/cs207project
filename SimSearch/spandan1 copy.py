from scipy.stats import norm
import random
import os
import numpy as np
from WrappedDB import WrappedDB
import sys
sys.path.append('../')
from timeseries import TimeSeries
from _corr import kernel_dist
from cs207rbtree import redblackDB

x=[];
v=[];

def tsmaker(m, s, j):
    t = list(np.arange(0.0, 1.0, 0.01))
    v = norm.pdf(t, m, s) + j*np.random.randn(100)
    return TimeSeries(values=v,times=t)

#[{1: <dist>, 2: <dist>, }_1, {}_2, ... {}_20] to
# (1,2);(2,3)....|(3,4);.....|
def encodeVantageDistances(decoded):
	dbstring = []
	for distances in decoded:
		distancestring = []
		for k, v in distances.items():
			distancestring.append("(" + str(k) + "," + str(v) + ")")
		dbstring.append(';'.join(distancestring))
	return '|'.join(dbstring)

# (1,2);(2,3)....|(3,4);.....| to
#[{1: <dist>, 2: <dist>, }_1, {}_2, ... {}_20]
def decodeVantageDistances(encoded):
	distances_from_vantage_points = []
	vantagePoints = encoded.split('|')
	for point in vantagePoints:
		dict_distances = {}
		items = point.split(';')
		for item in items:
			# Grab key and value
			split = item.split(',')
			key = int(split[0][1:])
			value = float(split[1][:-1])
			dict_distances[key] = value
		distances_from_vantage_points.append(dict_distances)
	return distances_from_vantage_points

def encodeTimeSeries(decoded):
	for timeSeries in decoded:
		items = timeSeries.items()
		encodedTimeSeries = []
		for (time, value) in items:
			encodedTimeSeries.append("(" + str(time) + "," + str(value) + ")")
		return ';'.join(encodedTimeSeries)

def decodeTimeSeries(encoded):
	itemStrings = encodedTimeSeries.split(';')
	t = []
	v = []
	for itemString in itemStrings:
		timeValuePair = itemString.split(',')

		if len(timeValuePair) != 2:
			raise ValueError('Time series string is malformed')

		time = timeValuePair[0]
		value = timeValuePair[1]
		if len(time) < 2 or len(value) < 2:
			raise ValueError('Time series string is malformed')			
		
		time = time[1:]
		value = value[:-1]

		# This might throw ValueError if time and value could not be converted to floats
		t.append(float(time))
		v.append(float(value))

	z = TimeSeries(values=v, times=t)
	return z


	
def encodeVantagePoints(decoded):
	""""""

def decodeVantagePoints(encoded):
	""""""



 # Get distance from vantage points from DB, and if its not there then proceed
# os.remove('distanceFromVantagePoints.dbdb')
db = redblackDB.connect("distanceFromVantagePoints.dbdb")
db_vantagepoints = redblackDB.connect("vantagePoints.dbdb")
db_data = redblackDB.connect("timeseriesdata.dbdb")

dbKey = 'encodedDistance'
dbKey_vantagepoint ='vantagePoints'
dbKey_data = 'timeseriesdata'

distances_from_vantage_points = []
# Check if it is in DB
try:
	print("getting from storage") 
	encodedDistances = db.get(dbKey)
	distances_from_vantage_points = decodeVantageDistances(encodedDistances)
	print(distances_from_vantage_points[19])
except KeyError:
	# Calculate and cache on disk
	print('Not stored in disk, calculate distances')
	num_vantage_points = 20
	num_of_timeseries = 1000
	

	#generation of 1000 time series
	for i in range(0,num_of_timeseries):
		ts=tsmaker(4,2,8)
		vals=ts.values()
		x.append(ts)

	print(x)

	#generate 20 vantage points 
	indices=random.sample(range(0,num_of_timeseries),num_vantage_points)
	for i in range(0,num_vantage_points):
		v.append(x[indices[i]])

	print(v)

	#Find distance of all points from each vantage point, store in array of dictionaries.
	for i in range(0,num_vantage_points):
		print('Working on vantage point: ', i)
		dict_distances={};
		for j in range(0,num_of_timeseries):
			distance_bw=kernel_dist(v[i],x[j])
			dict_distances[j]=distance_bw
		distances_from_vantage_points.append(dict_distances)
	db.set(dbKey, encodeVantageDistances(distances_from_vantage_points))
	db.commit()

	#Store the 20 vantage points into dictionary


	#store the 1000 time series into dictionary




#generate random test sample for test series - 
test_ts=tsmaker(3,2,4)

#print(v[1])
corr=0
closest='dummy'
#Find closest vantage point
for i in range(0,20):
	print("Finding closest")
	print(i)
	if kernel_dist(test_ts,v[i])>corr:
		corr=kernel_dist(test_ts,v[i])
		closest=i

#Define region between them - 
max_region=2*corr
remaining_time_series=[];

distances_from_closest= distances_from_vantage_points[closest];

for index in distances_from_closest.keys():
	distance=distances_from_closest[index]
	if distance>max_region:
		del distances_from_closest[index]

final_distances=[]

#find top-n-cut in this
for i in distances_from_closest.keys():
	distance_from_test_sample=kernel_dist(x[i],test_ts)
	final_distances.append((i,distance_from_test_sample))
final_distances.sort(key=lambda x:x[1])

# final_distances
indexes_and_distances_of_top_20=final_distances[1:20]
print(indexes_and_distances_of_top_20)

