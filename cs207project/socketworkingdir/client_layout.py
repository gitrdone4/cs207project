# CLIENT

import sys
from serialization import serialize, Deserializer
from socket import socket, AF_INET, SOCK_STREAM
import json 
import numpy as np

s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 20001))

# STEP 1 -- CLIENT PREPARES INPUT IN JSON AND THEN SERIALIZES IT (input format -> json -> byte)
# if they are sending a new time series it might look like this
# import
external_ts_inpt = np.loadtxt(sys.argv[1])
# a list of dicts - an easy jsonifiable format
ts_for_json = [] 
for row in external_ts_inpt:
	ts_for_json.append({"time":row[0],"value":row[1]})
# to json
external_ts_json = json.dumps(ts_for_json, sort_keys=True)
# to byte
external_ts_byte = serialize(external_ts_json)

# STEP 2 -- CLIENT SENDS MSG
s.send(external_ts_byte)

# STEP 3 -- CLIENT RECEIVES MSG FROM SERVER
msg = s.recv(8192)

# STEP 4 -- CLIENT CONVERTS RECEIVED MSG TO JSON
ds = Deserializer()
ds.append(msg)
if ds.ready():
	best_match = ds.deserialize()

print(best_match)
