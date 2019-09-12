import numpy
import string
import datetime
import sys
import os
from datetime import datetime
from datetime import timedelta

# test.in: 
#  line: 3 .mseed files corresponding to 1 event (N, E, Z components)

# test.out: -> GDP model output 
#  line: 4 outputs: network name, station name, label (P/S), time 

# test.out.database: -> PNSN labelled event data
#  line: 6 outputs: network name, station name, label (P/S), time, quality measure (i/e/None), event type (EQP, EQS, ...)

# ------------------- dirs need updating ---------------
model_file = 'test.out'
truth_file = 'test.out.database'
outp_name = 'comparison.out'

# Read in PNSN data and store it as an array
truth_arr = []
with open(truth_file) as f:
    for line in f:
        tmp = line.split()
        formatted_time = datetime.strptime(tmp[3], "%Y-%m-%dT%H:%M:%S.%f") # parse str to datetime object
        truth_arr.append([tmp[0], tmp[1], tmp[2], formatted_time, tmp[4], tmp[5]])

print(truth_arr)

# time search algorithm for model data
# ------ there must be more efficient way to do this?
def search_model_file(event):
    t = event[3] 
    t_lower = t - timedelta(seconds=5)
    t_upper = t + timedelta(seconds=5) 
    with open(model_file) as f:
        for line in f:
            outp = [event[5], 'F', numpy.nan] # template output
            tmp = line.split()
            formatted_time = datetime.strptime(tmp[3], "%Y-%m-%dT%H:%M:%S.%f") # parse str to datetime object
            tmp[3] = formatted_time
            # if network name, seismic station name match and phase arrival time is within 10 s window, return True
            if event[0] == tmp[0] and event[1] == tmp[1] and formatted_time > t_lower and formatted_time < t_upper:
                # phase check (T if the same, F otherwise)
                if event[2] == tmp[2]:
                    outp[1] = 'T'
                # offset
                offset = abs(formatted_time - t)
                outp[2] = offset.total_seconds()
                return [True, outp]
    return [False, ['NOF', numpy.nan, numpy.nan]] # NOF code: not found, nan, nan

# p and s wave search is messy 
    

# Check whether PNSN event was detected by the GDP model and write output to file
outp_file = open(outp_name, 'w')

for event in truth_arr:
    search_result = search_model_file(event)
    res = search_result[1]
    print(res)
    outp_file.write(str(res[0]) + " " + str(res[1]) + " " + str(res[2]) + '\n' )
outp_file.close()

    
    
    