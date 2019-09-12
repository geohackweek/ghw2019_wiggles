import numpy
import string
import datetime
import sys
import os
import csv
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
fudge_factor = timedelta(seconds=27)

# ------------------
# Read in PNSN data and store it as an array
truth_arr = []
with open(truth_file) as f:
    for line in f:
        tmp = line.split()
        formatted_time = datetime.strptime(tmp[3], "%Y-%m-%dT%H:%M:%S.%f") # parse str to datetime object
        truth_arr.append([tmp[0], tmp[1], tmp[2], formatted_time, tmp[4], tmp[5]])
        
        
networks = ['CC', 'PP', 'KK']
stations = ['SIFT', 'RUSH', 'PR05', 'OBSR']
phases = ['P', 'S']
model_dict = {}

# create dictionary keys
for netw in networks:
    for stat in stations:
        for phase in phases:
            model_dict[netw + "-" + stat + "-" + phase] = []
            
# read model file and add parsed datetime obj to dict
with open(model_file) as f:
        for line in f:
            tmp = line.split()
            formatted_time = datetime.strptime(tmp[3], "%Y-%m-%dT%H:%M:%S.%f") # parse str to datetime object
            model_dict[tmp[0] + "-" + tmp[1] + "-" + tmp[2]].append(formatted_time) 

# search for arrivals within +- 5s window
def key_lookup(event):
    t = event[3] 
    t_lower = t - timedelta(seconds=5)
    t_upper = t + timedelta(seconds=5) 
    primary_key = event[0] + "-" + event[1] + "-" + event[2]
    opp_phase = 'P'
    if event[2] == 'P':
        opp_phase = 'S'
    secondary_key = event[0] + "-" + event[1] + "-" + opp_phase
    
    if primary_key in model_dict.keys(): #same phase detected
        times = [event[2], model_dict[primary_key]]
    elif secondary_key in model_dict.keys(): # opposite phase
        times = [opp_phase, model_dict[secondary_key]]
    else: # not detected
        times = ['N', [numpy.nan]] 
    return times


outp_file = open(outp_name, 'w')
for event in truth_arr:
    phases_times = key_lookup(event)
    res = phases_times[1]
    phase = phases_times[0]
    # filter events in +-5s time window
    t = event[3] 
    t_lower = t - timedelta(seconds=5)
    t_upper = t + timedelta(seconds=5) 
    arrivals_window = []
    outp_file.write(str(event[5]) + " " + str(phase))
    for time in res:
        if time > t_lower and time < t_upper:
            offset = abs(t - time)
            offset = offset.total_seconds()
            arrivals_window.append(time)
            outp_file.write(" " + str(offset))
    outp_file.write('\n')
outp_file.close()


