from timeseries import TimeSeries
import numpy as np

class ArrayTimeSeries(TimeSeries):
    
    def __init__(self, initial_data):
        # Confirm inital_data is a sequence. 
        try: 
                _ = (e for e in initial_data)
        except TypeError:
                print(initial_data, "is not iterable")
                raise TypeError
        else:
                self.data = np.array(initial_data)
 