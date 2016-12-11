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
            # In the former case the client sends an id, in the latter the full time series dataset.  
            # I believe this is the purpose of the TSDBOp code we are given.
            # How do we currently determine if the time series already exists or is new?

            # STEP 3 -- PERFORM SIM SEARCH. 
            # I think sim search should return a dictionary of the closest time series keyed by distances is that right?
            sim_search_out = {40:"timeseries425", 30:"timeseries312"}
            best_match = json.dumps(sim_search_out, sort_keys=True)

            # STEP 4 -- SERIALIZE AGAIN AND SEND BACK TO CLIENT (json->byte conversion)
            self.request.send(serialize(best_match))
            
if __name__ == '__main__':
    serv = TCPServer(('', 20001), EchoHandler) 
    serv.serve_forever()