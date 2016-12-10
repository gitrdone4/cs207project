from scipy.stats import norm
import random
import os
import numpy as np
import sys
sys.path.append('../timeseries')
from timeseries import TimeSeries
from arraytimeseries import ArrayTimeSeries
from sizedcontainertimeseriesinterface import SizedContainerTimeSeriesInterface
sys.path.append('../cs207rbtree')
import redblackDB
sys.path.append('../SimSearch')
from _corr import kernel_dist
import pprint

# py.test --doctest-modules  --cov --cov-report term-missing Distance_from_known_ts.py

def load_ts_file(filepath):
    '''
    Takes in file and reads time series from it

	Parameters
	----------
	filepath: path of the file 
	
	Returns
	-------
	timeSeries object : TimeSeries class

	>>> ts=load_ts_file('169975.dat_folded.txt')

	>>> ts._values[0]
	15.137
    '''

#Only considers the first two columns of the text file (other columns are discarded)
#Only evaluates time values between 0 and 1
#First column is presumed to be times and second column is presumed to be light curve values.
    data = np.loadtxt(filepath, delimiter=' ',dtype = str)
    clean_input = []
    for i in range(len(data)):
        row = data[i].split("\\t")
        clean_input.append([float(row[0][2:]),float(row[1])])
    data = np.array(clean_input)

    _ , indices = np.unique(data[:, 0], return_index=True)

    data = data[indices, :]
    times, values = data.T
    full_ts = TimeSeries(times=list(times),values=list(values))
    interpolated_ts = full_ts.interpolate(list(np.arange(0.0, 1.0, (1.0 /100))))
    full_ts_interpolated = TimeSeries(times=list(np.arange(0.0, 1.0, (1.0 /100))),values=list(interpolated_ts))
    return full_ts_interpolated

if len(sys.argv)<2:
	raise ValueError("No input file containing time series passed")
else:
	test_ts=load_ts_file(sys.argv[1])

num_vantage_points = 20
num_of_timeseries = 1000
num_top=int(sys.argv[2])

def tsmaker(m, s, j):
    '''
    Creates a random time series of 100 elements

	Parameters
	----------
	m,s,j: parameters of the function norm.pdf

	Returns
	-------
	timeSeries object : TimeSeries class

	>>> ts = tsmaker(2,3,4)

	>>> ts._times[0]
	0.0
    '''
    t = list(np.arange(0.0, 1.0, 0.01))
    v = norm.pdf(t, m, s) + j*np.random.randn(100)
    return TimeSeries(values=v,times=t)

#[{1: <dist>, 2: <dist>, }_1, {}_2, ... {}_20] to
# (1,2);(2,3)....|(3,4);.....|
def encodeVantagePoints(decoded):
	'''
	Encodes the vantage point to a string so that it can be stored

	Parameters
	----------
	Decoded: Any list that is to be encoded

	Returns
	-------
	string

	>>> ts=encodeVantagePoints({1:(1,2)})
	>>> ts[1]
	'1'
	'''
	# dbstring = []
	# for distances in decoded:
	distancestring = []
	for k, v in decoded.items():
		distancestring.append("(" + str(k) + "," + str(v) + ")")
	encodedString = ';'.join(distancestring)
	return encodedString
	# dbstring.append(';'.join(distancestring))
	# return '|'.join(dbstring)

# (1,2);(2,3)....|(3,4);.....| to
#[{1: <dist>, 2: <dist>, }_1, {}_2, ... {}_20]
def decodeVantagePoints(encoded):
	'''
	>>> ts=decodeVantagePoints('(1,2);(2,3)')
	>>> ts
	{1: 2.0, 2: 3.0}
	'''
	dict_distances = {}
	items = encoded.split(';')
	for item in items:
		# Grab key and value
		split = item.split(',')
		key = int(split[0][1:])
		value = float(split[1][:-1])
		dict_distances[key] = value
	return dict_distances

def encodeTimeSeries(timeSeries):
	"""
	Takes in time series object and transforms it into a string.
	
	Parameters
	----------
	timeSeries: Concrete class of SizedContainerTimeSeriesInterface
	
	Returns
	-------
	String representation of time series object, where each time and value is encoded in 
	"(t,v)" and separated with ";"

	>>> ts = TimeSeries(values=[0, 2, -1, 0.5, 0], times=[1, 1.5, 2, 2.5, 10])
	>>> k=encodeTimeSeries(ts)
	>>> k
	'(1,0);(1.5,2);(2,-1);(2.5,0.5);(10,0)'
	"""
	items = timeSeries.items()
	encodedTimeSeries = []
	for (time, value) in items:
		encodedTimeSeries.append("(" + str(time) + "," + str(value) + ")")
	return ';'.join(encodedTimeSeries)

# Takes in encoded time series and transforms it into a TimeSeries object
# Raise ValueError whenever improper
def decodeTimeSeries(encodedTimeSeries):
	"""
	Takes in time series string and transforms it into a time series object.
	Raises ValueError when the input string is malformed.
	
	Parameters
	----------
	String representation of time series object, where each time and value is encoded in 
	"(t,v)" and separated with ";"
	
	Returns
	-------
	timeSeries: TimeSeries class

	>>> ts = TimeSeries(values=[0, 2, -1, 0.5, 0], times=[1, 1.5, 2, 2.5, 10])
	>>> encodedString = encodeTimeSeries(ts)
	>>> k=decodeTimeSeries(encodedString)
	>>> k
	TimeSeries(Length: 5, [0.0, 2.0, -1.0, 0.5, 0.0])
	"""
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

def read_ts(i):
	'''
	Read Time Series from disk

	Parameters
	----------
	i:ID of the time series to be read from disk

	Returns
	-------
	time series object
	'''
	filename='ts-'+str(i)+'.txt'
	t=[]
	v=[]
	lines = [line.rstrip('\n') for line in open(filename)]
	for line in lines:
		(time,val)=line.split(" ")
		t.append(time)
		v.append(float(val))
	ts=TimeSeries(values=v,times=t)
	return ts

def write_ts(ts,i):
    """ Write light curve to disk as space delimited text file"""
    '''
    Write light curve to disk as space delimited text file
	
	Parameters
	----------
	ts: time series object
	i : a counter to be appended to the file name where it is stored 
	Returns
	-------
	None. 
    '''
    path = "ts-{}.txt".format(i)
    datafile_id = open(path, 'wb')
    data = np.array([ts._times, ts._values])
    data = data.T

    np.savetxt(datafile_id, data, fmt=['%.3f','%8f'])
    datafile_id.close()

 # Get distance from vantage points from DB, and if its not there then proceed

db = redblackDB.connect("distanceFromVantagePoints.dbdb")
db_vantagepoints = redblackDB.connect("vantagePoints.dbdb")
db_data = redblackDB.connect("timeseriesdata.dbdb")

distances_from_vantage_points = []
v=[]
x=[]

try:

	#try to read the file containing the dictionary of vantagepoint_id:vantagepoint_timeseries

	#try to check if there are 20 redblack trees. One of these will be read in the later part oft he code. 
	#db_data.get('hello')
	#raise KeyError
	file=open('vantagepointids.txt')
	print("Red Black trees already found!")
	#dbfilename='db_vantagepoints'+closest
	#vantagedb=redblackDB.connect(db_file_name+'.dbdb')
	#vantagedb.get()
	#for i in range(num_vantage_points):
	#	key='v'+str(i)
	#	decodedVantagePoints=db_vantagepoints.get(key)
	#	v.append(decodeTimeSeries(decodedVantagePoints))
	#	distances_from_vantage_points.append(decodeVantagePoints(db.get(key)))

	#for i in range(num_of_timeseries):
	#	key='x' + str(i)
	#	x.append(decodeTimeSeries(db_data.get(key)))
	
except FileNotFoundError:
	
	# Calculate and cache on disk
	print('Not stored in disk, calculate distances')

	#generate 20 random indices as vantage point id's
	vantage_point_ids=random.sample(range(num_of_timeseries), num_vantage_points)
	filename='vantagepointids.txt'
	fileh=open(filename,'w')
	fileh.write(str(vantage_point_ids))
	#print(len(vantage_point_ids))
	vpcounter=1
	#generation of 1000 time series
	for i in range(num_of_timeseries):
		ts=tsmaker(4,2,8)
		write_ts(ts,i)
		x.append(ts)
		#db_data.set('x' + str(i), encodeTimeSeries(ts))
		#db_data.commit()
		#if vantage point then retain in v
		if i in vantage_point_ids:
			v.append(ts)

	
	for i in range(num_vantage_points):
		print('Working on vantage point: ', i)
		db_file_name='db_vantagepoints'+str(i)
		vantagedb=redblackDB.connect(db_file_name+'.dbdb')
		dict_distances = {}
		for j in range(num_of_timeseries):
			distance_bw=kernel_dist(v[i],x[j])
			dict_distances[j]=distance_bw
		for key in dict_distances.keys():
			#print("I am at key",key)
			val=dict_distances[key]
			#print("val is",val)
			vantagedb.set(str(val),str(key))
			#print("I set stuff")
		vantagedb.commit()
	

corr=0
closest='dummy'

filename='vantagepointids.txt'
fileh=open(filename,'r')
vantageids=fileh.read()
vantageids=vantageids[1:len(vantageids)-1]
vantageids.replace(" ","")
list=vantageids.split(',')
#print('vantageids are',vantageids)
v=[]
for vp in list:
	ts=read_ts(vp.replace(" ",""))
	v.append(ts)

#Find closest vantage point
for i in range(num_vantage_points):
	if kernel_dist(test_ts,v[i]) > corr:
		corr = kernel_dist(test_ts,v[i])
		closest = str(i)



#Define region between them
max_region=2*corr

dbfilename='db_vantagepoints'+closest
vantagedb=redblackDB.connect(dbfilename+'.dbdb')
dist=vantagedb.chop(str(max_region))
rboutputs={}
for i in dist:
	(a,b)=i
	rboutputs[b]=a;


sortedrbouts=sorted(rboutputs, key=rboutputs.get, reverse=True)[:num_top]
print('IDs of the top ',num_top,'time series are',','.join(map(str,sortedrbouts)))
