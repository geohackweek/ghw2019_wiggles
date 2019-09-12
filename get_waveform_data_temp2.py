#----- import modules

import os.path
import time
import obspy
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from time_series import *

#----- parameters to modify 

outputdir = '/srv/shared/wiggles'
inputfile = 'arrivals.csv'
TBeforeArrival = 10.
TAfterArrival = 10.
LeapSecondFudge = 27  # Fudge factor.  Subtract this from all times.
highpassfiltercorner = 0.5
timebuffer = 15.
common_sample_rate = 100.  # in Hz
client = Client("IRIS")
label = 'test'

#---- Function to read infile

import csv
def parse_input_file(filename):
    request = {}
    for t in ['EQS','EQP','SUS','SUP','THS','THP','SNS','SNP','PXS','PXP']:
        request[t] = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            pick = {}
            pick['event_type'] = row[0].strip()
            pick['time'] = row[1].strip()
            pick['sta'] = row[2].strip()
            pick['net'] = row[3].strip()
            pick['loc'] = row[4].strip()
            pick['chan'] = row[5].strip()
            pick['pick_type'] = row[6].strip()
            pick['quality'] = row[7].strip()
            pick['who'] = row[8].strip()
            #print(pick) 
            key = "{}{}".format(pick['event_type'], pick['pick_type'])
            request[key].append(pick)
    return request

#----- Start the main program

etype_dict = parse_input_file(inputfile)
taperlen = (3./highpassfiltercorner)

#----- Sweep through each arrival, download Z+N+E data, write as mseed file

n = 0
#etype_list = ['EQP','SUP','THP','SNP','PXP']
etype_list = ['EQS','SUS','THS','SNS','PXS']
#etype_list = ['EQS','EQP','SUS','SUP','THS','THP','SNS','SNP','PXS','PXP']
for etype in etype_list:
    f0 = open(labepython get _waveform_data_temp1.pyl + "." + etype + ".in",'a')
    f1 = open(label + "." + etype + ".out.database",'a')
    n = 0
    for row in etype_dict[etype]:
#    if ( n < 8 ):   # put on the brakes, just for testing
        time.sleep(0.01)  # make sure we don't request data too fast
        net = row['net']
        stat = row['sta']
        loc = row['loc']
        if ( loc == "" ):
            loc = "--"
        chan = row['chan']
        phase = row['pick_type']
        qual = row['quality']
        sncl = net + '.' + stat + '.' + loc + '.' + chan
        netstatloc = net + '.' + stat + '.' + loc 
        utoriginal = float(row['time'])
        unixtime = float(row['time']) - LeapSecondFudge
        ut = UTCDateTime(unixtime)
        T1 = ut - TBeforeArrival - timebuffer
        T2 = ut + TAfterArrival + timebuffer
        T = UTCDateTime(utoriginal)
#        print("TRYING: " + sncl + " " + str(ut) + " " + str(T1) + " " + str(row['time'])  )
        minlen = T2 - T1 - 1
        strdate = str(T.year) + str(T.month).zfill(2) + str(T.day).zfill(2) + \
                  str(T.hour).zfill(2) + str(T1.minute).zfill(2) + \
                  str(T.second).zfill(2)
        fname = sncl + "." + strdate + ".mseed"
        chan = chan[:2] + "Z"
        checkfile = outputdir + "/" + etype + "/" + netstatloc + "." + chan + "." + strdate + ".mseed"
        if ( os.path.isfile(checkfile) is True ):
            print("Already downloaded ",checkfile)
        else:
          try:
            chan = chan[:2] + "N"
            fnameN = outputdir + "/" + etype + "/" + netstatloc + "." + chan + "." + strdate + ".mseed"
            stN = client.get_waveforms(network=net, station=stat, location=loc, 
                                      channel=chan, starttime=T1, endtime=T2, 
                                      minimumlength = minlen, longestonly = True,
                                      attach_response = True )
            chan = chan[:2] + "E"
            fnameE = outputdir + "/" + etype + "/" + netstatloc + "." + chan + "." + strdate + ".mseed"
            stE = client.get_waveforms(network=net, station=stat, location=loc, 
                                      channel=chan, starttime=T1, endtime=T2, 
                                      minimumlength = minlen, longestonly = True,
                                      attach_response = True )
            chan = chan[:2] + "Z"
            fnameZ = outputdir + "/" + etype + "/" + netstatloc + "." + chan + "." + strdate + ".mseed"
            stZ = client.get_waveforms(network=net, station=stat, location=loc, 
                                      channel=chan, starttime=T1, endtime=T2, 
                                      minimumlength = minlen, longestonly = True,
                                      attach_response = True )
            #----- demean and taper the data
            stN.detrend(type='demean')
            stE.detrend(type='demean')
            stZ.detrend(type='demean')
            stN.taper(0.5, max_length = taperlen)
            stE.taper(0.5, max_length = taperlen)
            stZ.taper(0.5, max_length = taperlen)

            #----- if it's acceleration data, convert to velocity
            if ( chan[1:2] == 'N' ):
                stN.remove_response(output = 'VEL', pre_filt = ( 0.3, 0.5, 40., 45.))
                stE.remove_response(output = 'VEL', pre_filt = ( 0.3, 0.5, 40., 45.))
                stZ.remove_response(output = 'VEL', pre_filt = ( 0.3, 0.5, 40., 45.))
            elif ( chan[1:2] == 'H' ):
                iskip_response_removal = 1
            else:
                iskip_this_station = 1/0

            #----- high-pass filter everything above 1 Hz
            stN.filter('highpass', freq=highpassfiltercorner)
            stE.filter('highpass', freq=highpassfiltercorner)
            stZ.filter('highpass', freq=highpassfiltercorner)

            #----- make sure it's the correct sampling rate
            correct_sample_rate(stN, common_sample_rate)
            correct_sample_rate(stE, common_sample_rate)
            correct_sample_rate(stZ, common_sample_rate)

            #----- trim data to common start/endtimes and Npoints
            trim_to_common_times(stN, stE, stZ, timebuffer)

            #----- write out the data to an .mseed file
            stN.write(fnameN, format='MSEED')
            stE.write(fnameE, format='MSEED')
            stZ.write(fnameZ, format='MSEED')

            f0.write( str(fnameN) + " " + str(fnameE) + " " + str(fnameZ) + '\n' )
            f1.write( net + " " + stat + " " + phase + " " + str(ut)[:-1] + " " + str(qual) + " " + etype + '\n' )  # AZ TRO P 2016-06-10T00:03:53.808300
            print("Downloaded ",fname)
            n += 1
          except:
            print("Download failed for ",fname)

    f0.close()
    f1.close()

