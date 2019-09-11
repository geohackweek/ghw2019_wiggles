#!/home/ahutko/anaconda3/bin/python

#----- import modules

import psycopg2
import obspy
from obspy import UTCDateTime
from obspy.clients.fdsn import Client

#----- parameters to modify 

outputdir = '/srv/shared/wiggles'
inputfile = 'Labeled_arrivals_from_UWdatabase.txt'
TBeforeArrival = 5.
TAfterArrival = 5.
highpassfiltercorner = 1.0
timebuffer = 15.
common_sample_rate = 100.  # in Hz
client = Client("IRIS")

#---- Function to read infile

def parse_input_file(filename):
    request = {}
    for t in ['EQS','EQP','SUS','SUP','THS','THP','SNS','SNP','PXS','PXP']:
        request[t] = []
    with open(filename, 'r') as infile:
        for line in infile: 
            pick = {}
            pick_line = line.split(',')
            pick['event_type'] = pick_line[0].replace('[','').replace("'",'').strip()
            pick['time'] = pick_line[1].replace("'",'').strip()
            pick['sta'] = pick_line[2].replace("'",'').strip()
            pick['net'] = pick_line[3].replace("'",'').strip()
            pick['loc'] = pick_line[4].replace("'",'').strip()
            pick['chan'] = pick_line[5].replace("'",'').strip()
            pick['pick_type'] = pick_line[6].replace("'",'').strip()
            pick['quality'] = pick_line[7].replace("'",'').strip()
            pick['who'] = pick_line[8].replace(']','').replace("'",'').strip()
            #print(pick) 
            key = "{}{}".format(pick['event_type'], pick['pick_type'])
            print(key)
            request[key].append(pick)

parse_input_file('Labeled_arrivals_from_UWdatabase.txt')


taperlen = (2./highpassfiltercorner)

f0 = open(label + ".in",'w')
f1 = open(label + ".out.database",'w')

#----- Sweep through each arrival, download Z+N+E data, write as mseed file

n = 0
downloaded_netstatloc = []
for record in cursor:
#  if ( n < 10 ):
    n += 1
    net = record[4]
    stat = record[3]
    chan = record[9]
    loc = record[10]
    phase = record[11]
    qual = record[12]
    if ( loc == "  " ):
        loc = "--"
    sncl = net + '.' + stat + '.' + loc + '.' + chan
    netstatloc = net + '.' + stat + '.' + loc 
    if ( netstatloc not in downloaded_netstatloc ):
        downloaded_netstatloc.append(netstatloc)
        unixtime = record[2]
        ut = UTCDateTime(unixtime)
        T1 = ut - TAfterArrival - timebuffer
        T2 = ut + TBeforeArrival + timebuffer
        minlen = T2 - T1 - 1
        strdate = str(T1.year) + str(T1.month).zfill(2) + str(T1.day).zfill(2) + \
                  str(T1.hour).zfill(2) + str(T1.minute).zfill(2) + \
                  str(T1.second).zfill(2)
        fname = sncl + "." + strdate + ".mseed"
        try:
            chan = chan[:2] + "N"
            fnameN = netstatloc + "." + chan + "." + strdate + ".mseed"
            stN = client.get_waveforms(network=net, station=stat, location=loc, 
                                      channel=chan, starttime=T1, endtime=T2, 
                                      minimumlength = minlen, longestonly = True,
                                      attach_response = True )
            chan = chan[:2] + "E"
            fnameE = netstatloc + "." + chan + "." + strdate + ".mseed"
            stE = client.get_waveforms(network=net, station=stat, location=loc, 
                                      channel=chan, starttime=T1, endtime=T2, 
                                      minimumlength = minlen, longestonly = True,
                                      attach_response = True )
            chan = chan[:2] + "Z"
            fnameZ = netstatloc + "." + chan + "." + strdate + ".mseed"
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
                stN.remove_response(output = 'VEL', pre_filt( 0.3, 0.5, 40., 45.))
                stE.remove_response(output = 'VEL', pre_filt( 0.3, 0.5, 40., 45.))
                stZ.remove_response(output = 'VEL', pre_filt( 0.3, 0.5, 40., 45.))
            elif ( chan[1:2] == 'H' ):
                iskip_response_removal = 1
            else:
                iskip_this_station = 1/0

            #----- high-pass filter everything above 1 Hz
            stN.highpass(highpassfiltercorner)
            stE.highpass(highpassfiltercorner)
            stZ.highpass(highpassfiltercorner)

            #----- make sure it's the correct sampling rate
            correct_sample_rate(stN, common_sample_rate)
            correct_sample_rate(stE, common_sample_rate)
            correct_sample_rate(stZ, common_sample_rate)

            #----- trim data to common start/endtimes and Npoints
            trim_to_common_times(stN, stE, stZ)

            #----- write out the data to an .mseed file
            stN.write(fnameN, format='MSEED')
            stE.write(fnameE, format='MSEED')
            stZ.write(fnameZ, format='MSEED')

            f0.write( str(fnameN) + " " + str(fnameE) + " " + str(fnameZ) + '\n' )
            f1.write( net + " " + stat + " " + phase + " " + str(ut)[:-1] + " " + str(qual) + '\n' )  # AZ TRO P 2016-06-10T00:03:53.808300
            print("Downloaded ",fname)
        except:
            print("Download failed for ",fname)

f0.close()
f1.close()

