import numpy
import math
import string
import datetime
import sys
import os
import csv
from datetime import datetime
from datetime import timedelta

# params
fudge_factor = timedelta(seconds=27)
padding_time = 10

# file dirs
parsed_arrivals = []
model_in = []
model_out = []
comp_out = []
for etype in ['EQS','EQP','SUS','SUP','THS','THP','SNS','SNP','PXS','PXP']:
    infile = "input_files/GPD." + etype + ".in"
    outfile = "output_files/GPD." + etype + ".out"
    arrival = "parsed_arrivals/" + etype + ".arrivals.txt"
    parsed_arrivals.append(arrival)
    model_in.append(infile)
    model_out.append(outfile)
    comp_out.append("comparison_out/comp." + etype + ".out")

# ------------------
# read in UW arrival times as an array
def read_arrivals_to_arr(filename):
    model_list = []
    with open(filename) as f:
        for ln in f:
            row = ln.split()
            model_list
            line = []
            line.extend([row[0].strip(), row[1].strip(), row[2].strip()])
            formatted_time = datetime.strptime(row[3], "%Y-%m-%dT%H:%M:%S.%f") - fudge_factor # parse str to datetime object
            line.extend([formatted_time, row[4].strip(), row[5].strip()])
            model_list.append(line)
    return model_list

def arrivals_to_dictionary(arrivals):
    picks = {}
    for arr in arrivals:
        key = datetime.strftime(arr[3], "%Y-%m-%dT%H:%M:%S.%f")
        picks[key] = arr

#def model_in_to_dictionary(file):
    
        
#def filter_arrivals(arrivals, model_in_arrivals):
    

# read in Caltech model output and create a dictionary
def read_output_to_dict(filename):
    model_dict = {}
    with open(filename) as f:
        for line in f:
            tmp = line.split()
            key = tmp[0] + "-" + tmp[1] + "-" + tmp[2]
            try: # fails if date is missing floating point numbers
                formatted_time = datetime.strptime(tmp[3], "%Y-%m-%dT%H:%M:%S.%f") # parse str to datetime object
                if key not in model_dict:
                    model_dict[key] = []
                model_dict[key].append(formatted_time) 
            except:
                pass
    return model_dict

# search for arrivals within +- 10s window
def key_lookup(event, phase, model_dict):
    t = event[3] 
    t_lower = t - timedelta(seconds=padding_time)
    t_upper = t + timedelta(seconds=padding_time) 
    key = event[0] + "-" + event[1] + "-" + phase
    times = []
    if key in model_dict.keys():
        times = model_dict[key]
        times = time_lookup(event[3], times)
    return times

def time_lookup(t, time_arr):
    t_lower = t - timedelta(seconds=padding_time)
    t_upper = t + timedelta(seconds=padding_time) 
    offsets = []
    for time in time_arr:
        if time > t_lower and time < t_upper:
            offset = abs(t - time)
            offset = offset.total_seconds()
            offsets.append(offset)
    return offsets 

def execute_script(arrival, inf, outf, comp_out):
    # write outputs to file
    outp_file = open(comp_out, 'w')
    truth_arr = read_arrivals_to_arr(arrival)
    truth_dict = arrivals_to_dictionary(truth_arr)
    # read .in data
    # filter arrivals
    
    model_dict = read_output_to_dict(outf)
    for event in truth_arr:
        phase = event[2]
        times = key_lookup(event, phase, model_dict)
        if len(times) == 0:
            if phase == 'P':
                phase = 'S'
            else:
                phase = 'P'
            times = key_lookup(event, phase, model_dict)
        if len(times) == 0:
            phase = 'N'
            times = ['nan']
        outp_file.write(str(event[5]) + " " + phase)
        for offset in times:
            outp_file.write(" " + str(offset))
        outp_file.write('\n')
    outp_file.close()   

for i in range(len(model_out)):
    execute_script(parsed_arrivals[i], model_in[i], model_out[i], comp_out[i])
    
