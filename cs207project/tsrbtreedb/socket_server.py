# SERVER

from socketserver import BaseRequestHandler, TCPServer
from cs207project.socketclient.serialization import serialize, Deserializer
import json
import cs207project.timeseries.arraytimeseries as ats
import numpy as np
from cs207project.tsrbtreedb.simsearch_interface import simsearch_by_id, simsearch_by_ts, rebuild_vp_indexs


# delete me when simsearch_interface is up and running
##############################################################
# def simsearch_by_id(id, n):
#     return {40:"idsearch154", 30:"idsearch231"}

# def simsearch_by_ts(ts, n):
#     return {57:"tssearch001", 31:"tssearch007"}, None, None
##############################################################

class EchoHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        while True:
            msg = self.request.recv(8192)
            if not msg:
                break

            # 1. byte to json to dict
            ds = Deserializer()
            ds.append(msg)
            if ds.ready():
                msg_dict = ds.deserialize()

            # 2. get proximity dictionary (e.g. 5 closest time series)
            if msg_dict["type"]=="with_id":
                proximity_dict = simsearch_by_id(msg_dict["id"],n=5) # simsearch_interface.py enters here
            elif msg_dict["type"]=="with_ts":
                # reconstruct time series
                times = np.array(msg_dict["ts"])[:,0]
                values = np.array(msg_dict["ts"])[:,1]
                full_ts = ats.ArrayTimeSeries(times=times,values=values)
                proximity_dict = simsearch_by_ts(full_ts,n=5)[0] # simsearch_interface.py enters here

            # 3. dictionary to json
            proximity_json = json.dumps(proximity_dict, sort_keys=True)

            # 4. json to byte and send back to client
            self.request.send(serialize(proximity_json))

            # After we've sent back the best matches to the client (which will be fast)
            # We want to kickoff rebuilding the vantage point databases to incorporate the newly
            # submitted TS (which is slow)
            # if ts_is_new: rebuild_vp_indexs()

if __name__ == '__main__':
    serv = TCPServer(('', 20001), EchoHandler)
    serv.serve_forever()

'''
# RETAINED TERMPORARILY IN CASE YOU'D LIKE TO REVISIT NOTES
# SERVER

from socketserver import BaseRequestHandler, TCPServer
from serialization import serialize, Deserializer
import json

class EchoHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        while True:
            msg = self.request.recv(8192)
            if not msg:
                break

            # STEP 1 -- DESERIALIZE MSG FROM CLIENT (byte->json conversion)
            ds = Deserializer()
            ds.append(msg)
            if ds.ready():
            	external_ts = ds.deserialize()

            # STEP 2 -- CONVERT FROM JSON TO A FORMAT CONDUCIVE TO SIM SEARCH
            # If we are passed a time series that already exists in the database then this conversion differs to
            # if we are passed a fresh one.

            # N: There's no easy way to check if ts already exists without converting.
            #  You're going to need to convert to an ats object or send as json (and I'll convert within simsearch)


            # In the former case the client sends an id, in the latter the full time series dataset.
            # I believe this is the purpose of the TSDBOp code we are given.
            # How do we currently determine if the time series already exists or is new?

            # N: Per above,the only way to check if a ts already exists is to run a sim search if see if any
            # existing time series have a distance of 0. (See my simsearch_by_ts method)

            # STEP 3 -- PERFORM SIM SEARCH.
            # I think sim search should return a dictionary of the closest time series keyed by distances is that right?
            sim_search_out = {40:"timeseries425", 30:"timeseries312"}
            #N: Yes, looks good. See simsearch_by_id method.
            best_match = json.dumps(sim_search_out, sort_keys=True)

            # STEP 4 -- SERIALIZE AGAIN AND SEND BACK TO CLIENT (json->byte conversion)
            self.request.send(serialize(best_match))

            # here is how I see this work flow working:
            # If sever receives an id:

            try:
                best_match_dict = simsearch_by_id(id,n=5)
                best_match = json.dumps(best_match_dict, sort_keys=True)
            except ValueError:
                raise ValueError("ID not found in time series DB")

            # Alternatively, if we're sent a time series to process:

            best_match_dict,ts_id,ts_is_new = simsearch_by_ts(ts,n=5)
            # ts_id can either be existing id (if ts already exists) or new id if it's new

            best_match = json.dumps(best_match_dict, sort_keys=True)

            # After we've sent back the best matches to the client (which will be fast)
            # We want to kickoff rebuilding the vantage point databases to incorporate the newly
            # submitted TS (which is slow)
            if ts_is_new: rebuild_vp_indexs()

if __name__ == '__main__':
    serv = TCPServer(('', 20001), EchoHandler)
    serv.serve_forever()
'''