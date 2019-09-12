import numpy
import math
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
"""
def read_arrivals_to_list(filename):
    '''Read arrivals csv file and stuff into 2-dim array'''
    model_list = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            model_list.append(row)
    return model_list
    

truth_arr = read_arrivals_to_list("arrivals.csv")
"""

with open(truth_file) as f:
    for line in f:
        tmp = line.split()
        formatted_time = datetime.strptime(tmp[3], "%Y-%m-%dT%H:%M:%S.%f") # parse str to datetime object
        truth_arr.append([tmp[0], tmp[1], tmp[2], formatted_time, tmp[4], tmp[5]])
    # datetime.fromtimestamp(float(time))
# 

def read_output_to_dict(filename):
    model_dict = {}
    with open(filename) as f:
        for line in f:
            tmp = line.split()
            key = tmp[0] + "-" + tmp[1] + "-" + tmp[2]
            formatted_time = datetime.strptime(tmp[3], "%Y-%m-%dT%H:%M:%S.%f") # parse str to datetime object
            if key not in model_dict:
                model_dict[key] = []
            model_dict[key].append(formatted_time) 
    return model_dict
model_dict = read_output_to_dict(model_file)

# search for arrivals within +- 5s window
def key_lookup(event, phase):
    t = event[3] 
    t_lower = t - timedelta(seconds=5)
    t_upper = t + timedelta(seconds=5) 
    key = event[0] + "-" + event[1] + "-" + phase
    times = []
    if key in model_dict.keys():
        times = model_dict[key]
        times = time_lookup(event[3], times)
    return times

def time_lookup(t, time_arr):
    t_lower = t - timedelta(seconds=5)
    t_upper = t + timedelta(seconds=5) 
    offsets = []
    for time in time_arr:
        if time > t_lower and time < t_upper:
            offset = abs(t - time)
            offset = offset.total_seconds()
            offsets.append(offset)
    return offsets 

outp_file = open(outp_name, 'w')
for event in truth_arr:
    phase = event[2]
    times = key_lookup(event, phase)
    print('times1:', times)
    if len(times) == 0:
        if phase == 'P':
            phase = 'S'
        else:
            phase = 'P'
        times = key_lookup(event, phase)
        print('time0:', times)
    if len(times) == 0:
        phase = 'N'
        times = ['nan']
        print('empty', times)
    outp_file.write(str(event[5]) + " " + phase)
    for offset in times:
        outp_file.write(" " + str(offset))
    outp_file.write('\n')
outp_file.close()