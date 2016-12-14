# SERVER

import json
import numpy as np
from socketserver import BaseRequestHandler, TCPServer
from cs207project.socketclient.serialization import serialize, Deserializer
import cs207project.timeseries.arraytimeseries as ats
from cs207project.tsrbtreedb.simsearch_interface import simsearch_by_id, simsearch_by_ts, rebuild_vp_indexs, get_by_id, add_ts,rebuild_if_needed
from cs207project.tsrbtreedb.settings import LIGHT_CURVES_DIR, DB_DIR

class EchoHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        while True:
            msg = self.request.recv(8192)
            if not msg:
                break

            # Step 1. byte to json to dict
            ds = Deserializer()
            ds.append(msg)
            if ds.ready():
                msg_dict = ds.deserialize()

            # Step 2. take different actions depending on message type
            # print(msg_dict)

            # Message type: get n_nearest ts for time series id
            if msg_dict["type"]=="with_id":
                n = int(msg_dict["n"])
                try:
                    payload = simsearch_by_id(msg_dict["id"],n) # simsearch_interface.py enters here
                except ValueError as ve:
                    payload = {'error_type':'ValueError','error':str(ve)}

            # Message type: get n nearest ts for array time series object
            elif msg_dict["type"]=="with_ts":
                # reconstruct time series
                n = int(msg_dict["n"])
                times = np.array(msg_dict["ts"])[:,0]
                values = np.array(msg_dict["ts"])[:,1]
                try:
                    full_ts = ats.ArrayTimeSeries(times=times,values=values)
                except ValueError as ve:
                    payload = {'error_type':'ValueError','error':str(ve)}
                else:
                    try:
                        n_closest_dict,tsid,is_new = simsearch_by_ts(full_ts,n)
                        payload = {'n_closest_dict':n_closest_dict,'tsid':tsid}
                    except ValueError as ve:
                        payload = {'error_type':'ValueError','error':str(ve)}

            # Message type: get time series from database for given id
            elif msg_dict["type"]=="get_by_id":
                tsid = msg_dict["ts"]
                try:
                    full_ts = get_by_id(tsid)
                    payload = {'tsid':tsid, "ts":list(zip(full_ts.times(),full_ts.values()))}
                except ValueError as ve:
                    payload = {'error_type':'ValueError','error':str(ve)}

            # Message type: save time series to database
            elif msg_dict["type"]=="save_ts_to_db":
                times = np.array(msg_dict["ts"])[:,0]
                values = np.array(msg_dict["ts"])[:,1]
                try:
                    full_ts = ats.ArrayTimeSeries(times=times,values=values)
                    tsid = add_ts(full_ts)
                    payload = {'tsid':tsid}
                except ValueError as ve:
                    payload = {'error_type':'ValueError','error':str(ve)}

            # Unrecognized message type
            else:
                payload = {'error_type':'ValueError','error':("Message type '%s' is unrecognized" % msg_dict["type"])}

            # Step 3. dictionary to json
            payload = json.dumps(payload)

            # Setp 4. json to byte and send back to client
            self.request.send(serialize(payload))

if __name__ == '__main__':
    rebuild_if_needed(LIGHT_CURVES_DIR, DB_DIR)
    serv = TCPServer(('', 20001), EchoHandler)
    serv.serve_forever()
