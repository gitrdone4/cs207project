# SERVER

import json
import numpy as np
from socketserver import BaseRequestHandler, TCPServer
from cs207project.socketclient.serialization import serialize, Deserializer
import cs207project.timeseries.arraytimeseries as ats
from cs207project.tsrbtreedb.simsearch_interface import simsearch_by_id, simsearch_by_ts, rebuild_vp_indexs


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
            # N: Let's ignore this one for now -- I think I've come up with a better way to handle this. 

if __name__ == '__main__':
    serv = TCPServer(('', 20001), EchoHandler)
    serv.serve_forever()
