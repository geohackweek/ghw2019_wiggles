import numpy
import math
import string
import datetime
import sys
import os
import csv
from datetime import datetime
from datetime import timedelta

# ------------------- dirs need updating ---------------
model_file = 'test.out'
truth_file = 'arrivals.csv'
outp_name = 'comparison.out'
fudge_factor = timedelta(seconds=27)

# ------------------
# Read in PNSN .csv data and store it as an array
truth_arr = []
def read_arrivals_to_list(filename):
    model_list = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            line = []
            line.extend([row[3].strip(), row[2].strip(), row[6].strip()])
            formatted_time = datetime.fromtimestamp(float(row[1].strip())) - fudge_factor
            print(formatted_time, datetime.fromtimestamp(float(row[1].strip())))
            
            line.extend([formatted_time, row[7].strip(), row[0].strip()+row[6].strip()])
            model_list.append(line)
    return model_list
truth_arr = read_arrivals_to_list(truth_file)

# read in Caltech model output and create a dictionary
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

# write outputs to file
outp_file = open(outp_name, 'w')
for event in truth_arr:
    phase = event[2]
    times = key_lookup(event, phase)
    if len(times) == 0:
        if phase == 'P':
            phase = 'S'
        else:
            phase = 'P'
        times = key_lookup(event, phase)
    if len(times) == 0:
        phase = 'N'
        times = ['nan']
    outp_file.write(str(event[5]) + " " + phase)
    for offset in times:
        outp_file.write(" " + str(offset))
    outp_file.write('\n')
outp_file.close()