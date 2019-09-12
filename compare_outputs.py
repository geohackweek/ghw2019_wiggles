import numpy
import string
import datetime
import sys
import os
from datetime import datetime
from datetime import timedelta

# ---------------- input file structure -----------------
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

# ------------------
# Read in PNSN data and store it as an array
truth_arr = []
with open(truth_file) as f:
    for line in f:
        tmp = line.split()
        formatted_time = datetime.strptime(tmp[3], "%Y-%m-%dT%H:%M:%S.%f") # parse str to datetime object
        truth_arr.append([tmp[0], tmp[1], tmp[2], formatted_time, tmp[4], tmp[5]])
        
print(truth_arr)

# time search algorithm for model data
def search_model_file(event):
    t = event[3] 
    t_lower = t - timedelta(seconds=5)
    t_upper = t + timedelta(seconds=5) 
    with open(model_file) as f:
        phase_check = False
        for line in f:
            outp = [event[5], 'N', numpy.nan] # template output: event type, phase (P/S/N), offset (float/NaN)
            tmp = line.split()
            formatted_time = datetime.strptime(tmp[3], "%Y-%m-%dT%H:%M:%S.%f") # parse str to datetime object
            tmp[3] = formatted_time
            
            if event[0] == tmp[0] and event[1] == tmp[1] and formatted_time > t_lower and formatted_time < t_upper:
                outp[1] = tmp[2]
                # offset
                offset = abs(formatted_time - t)
                outp[2] = offset.total_seconds()
                # phase check
                if event[2] == tmp[2]:
                    return [True, outp]
                else:
                    phase_check = True
    return [phase_check, outp]

# Check whether PNSN event was detected by the GDP model and write output to file
outp_file = open(outp_name, 'w')
for event in truth_arr:
    search_result = search_model_file(event)
    res = search_result[1]
    outp_file.write(str(res[0]) + " " + str(res[1]) + " " + str(res[2]) + '\n' )
outp_file.close()

    
    
    