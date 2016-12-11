# CLIENT

import sys
from serialization import serialize, Deserializer
from socket import socket, AF_INET, SOCK_STREAM
import json 

s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 20001))

# STEP 1 -- CLIENT PREPARES INPUT IN JSON AND THEN SERIALIZES IT (input format -> json -> byte)
# if they are sending a new time series it might look like this
external_ts_inpt = {0.002:'val1',.005:'val2',.9:'val3'}
external_ts_json = json.dumps(external_ts_inpt)
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
