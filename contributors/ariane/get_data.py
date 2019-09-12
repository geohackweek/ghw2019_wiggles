"""
Functions to download the waveforms and put them
at the right format to be read by GPD code
"""
import obspy
from obspy import UTCDateTime
from obspy.clients.fdsn import Client

import pandas as pd

from fractions import Fraction

def read_input_file(filename):
    """
    Read input file and return pandas dataframe

    Input:
        type filename: string
        filename: Input file
    Output:
        type data: pandas dataframe
        data: List of timings of phases
    """
    data = pd.read_csv(filename, sep=',', \
        header=None)
    data.columns = ['type', 'time', 'station', 'network', 'location', \
        'channel', 'label', 'quality', 'who']
    data = data.astype({'type':str, 'time':float, 'station':str, \
        'network':str, 'location':str, 'channel':str, 'label':str, \
        'quality':str, 'who':str})
    # Remove [ and ]
    data['type'] = data['type'].str.replace("[", "")
    data['who'] = data['who'].str.replace("]", "")
    # Remove '
    data['type'] = data['type'].str.replace("'", "")
    data['station'] = data['station'].str.replace("'", "")
    data['network'] = data['network'].str.replace("'", "")
    data['location'] = data['location'].str.replace("'", "")
    data['channel'] = data['channel'].str.replace("'", "")
    data['label'] = data['label'].str.replace("'", "")
    data['quality'] = data['quality'].str.replace("'", "")
    data['who'] = data['who'].str.replace("'", "")
    # Remove white spaces
    data['type'] = data['type'].str.strip()
    data['station'] = data['station'].str.strip()
    data['network'] = data['network'].str.strip()
    data['location'] = data['location'].str.strip()
    data['channel'] = data['channel'].str.strip()
    data['label'] = data['label'].str.strip()
    data['quality'] = data['quality'].str.strip()
    data['who'] = data['who'].str.strip()
    return data

def trim_to_common_times(st1,st2,st3, timebuffer):
    starttimelist = []
    starttimelist.append(st1[0].stats.starttime)
    starttimelist.append(st2[0].stats.starttime)
    starttimelist.append(st3[0].stats.starttime)
    endtimelist = []
    endtimelist.append(st1[0].stats.endtime)
    endtimelist.append(st2[0].stats.endtime)
    endtimelist.append(st3[0].stats.endtime)
    starttime = max(starttimelist) + timebuffer
    endtime = min(endtimelist) - timebuffer
    st1.trim(starttime,endtime)
    st2.trim(starttime,endtime)
    st3.trim(starttime,endtime)
    nptslist = []
    nptslist.append(st1[0].stats.npts)
    nptslist.append(st2[0].stats.npts)
    nptslist.append(st3[0].stats.npts)
    npts = min(nptslist)
    dt = st1[0].stats.delta
    if ( st1[0].stats.npts > npts ):
        tdiff = (st1[0].stats.npts - npts) * dt
        st1.trim(starttime,endtime-tdiff)
    if ( st2[0].stats.npts > npts ):
        tdiff = (st2[0].stats.npts - npts) * dt
        st2.trim(starttime,endtime-tdiff)
    if ( st3[0].stats.npts > npts ):
        tdiff = (st3[0].stats.npts - npts) * dt
        st3.trim(starttime,endtime-tdiff)
    return [st1, st2, st3]

def download_data(data, filename, directory, \
    LeapSecondFudge=27, \
    TBeforeArrival=10.0, \
    TAfterArrival=10.0, \
    timebuffer=15.0, \
    highpassfiltercorner=0.3, \
    common_sample_rate=100.0):
    """
    Download the data defined in the input file
    and write waveforms in mseed format in directory

    Input:
        type data: pandas dataframe
        data: List of timings of phase
        type directory: string
        directory: Where we store the mseed files
        type LeapSecondFudge: float
        LeapSecondFudge: Fudge factor. Subtract this from all times
    Output:
        None
        """
    client = Client('IRIS')
    taperlen = 2.0 /highpassfiltercorner
    
    for i in range(0, 2): #len(data)):
        unixtime = data['time'].iloc[i] - LeapSecondFudge
        ut = UTCDateTime(unixtime)
        T1 = ut - TBeforeArrival - timebuffer
        T2 = ut + TAfterArrival + timebuffer
        minlen = T2 - T1 - 1
        strdate = str(T1.year) + str(T1.month).zfill(2) + str(T1.day).zfill(2) + \
                  str(T1.hour).zfill(2) + str(T1.minute).zfill(2) + \
                  str(T1.second).zfill(2)
        network = data['network'].iloc[i]
        station = data['station'].iloc[i]
        location = data['location'].iloc[i]
        channel = data['channel'].iloc[i]
        if (len(location) > 0):
            sncl = network + '.' + station + '.' + location + '.' + channel
        else:
            sncl = network + '.' + station + '.' + channel
        fname = strdate + '.' + sncl + '.mseed'
        # If record is present download the data
        try:
            # North component
            channel = channel[:2] + 'N'
            if (len(location) > 0):
                sncl = network + '.' + station + '.' + location + '.' + channel
            else:
                sncl = network + '.' + station + '.' + channel
            fnameN = strdate + '.' + sncl + '.mseed'
            stN = client.get_waveforms(network=network, station=station, location=location, \
                channel=channel, starttime=T1, endtime=T2, minimumlength = minlen, \
                longestonly = True, attach_response = True )
            # East component
            channel = channel[:2] + 'E'
            if (len(location) > 0):
                sncl = network + '.' + station + '.' + location + '.' + channel
            else:
                sncl = network + '.' + station + '.' + channel
            fnameE = strdate + '.' + sncl + '.mseed'
            stE = client.get_waveforms(network=network, station=station, location=location, \
                channel=channel, starttime=T1, endtime=T2, minimumlength = minlen, \
                longestonly = True, attach_response = True )
            # Vertical component
            channel = channel[:2] + 'Z'
            if (len(location) > 0):
                sncl = network + '.' + station + '.' + location + '.' + channel
            else:
                sncl = network + '.' + station + '.' + channel
            fnameZ = strdate + '.' + sncl + '.mseed'
            stZ = client.get_waveforms(network=network, station=station, location=location, \
                channel=channel, starttime=T1, endtime=T2, minimumlength = minlen, \
                longestonly = True, attach_response = True )
            # Demean and taper the data
            stN.detrend(type='demean')
            stE.detrend(type='demean')
            stZ.detrend(type='demean')
            stN.taper(0.5, max_length=taperlen)
            stE.taper(0.5, max_length=taperlen)
            stZ.taper(0.5, max_length=taperlen)
            # If it's acceleration data, convert to velocity
            if (channel[1:2] == 'N'):
                stN.remove_response(output='VEL', pre_filt=(0.3, 0.5, 40.0, 45.0))
                stE.remove_response(output='VEL', pre_filt=(0.3, 0.5, 40.0, 45.0))
                stZ.remove_response(output='VEL', pre_filt=(0.3, 0.5, 40.0, 45.0))
            elif (channel[1:2] == 'H'):
                pass
            else:
                raise Exception('Not accelerometer nor high gain seismometer')
            # High-pass filter everything above 1 Hz
            stN.filter('highpass', freq=highpassfiltercorner)
            stE.filter('highpass', freq=highpassfiltercorner)
            stZ.filter('highpass', freq=highpassfiltercorner)
            # Correct sampling rate
            freq = stN[0].stats.sampling_rate
            if (freq != common_sample_rate):
                ratio = Fraction(int(freq), int(common_sample_rate))
                stN.interpolate(ratio.denominator * freq, method='lanczos', a=10)
                stN.decimate(ratio.numerator, no_filter=True)
            freq = stE[0].stats.sampling_rate
            if (freq != common_sample_rate):
                ratio = Fraction(int(freq), int(common_sample_rate))
                stE.interpolate(ratio.denominator * freq, method='lanczos', a=10)
                stE.decimate(ratio.numerator, no_filter=True)
            freq = stZ[0].stats.sampling_rate
            if (freq != common_sample_rate):
                ratio = Fraction(int(freq), int(common_sample_rate))
                stZ.interpolate(ratio.denominator * freq, method='lanczos', a=10)
                stZ.decimate(ratio.numerator, no_filter=True)
            # Trim data to common start/endtimes and Npoints
            trim_to_common_times(stN, stE, stZ, timebuffer)
            # Write out the data to an .mseed file
            stN.write(directory + '/' + fnameN, format='MSEED')
            stE.write(directory + '/' + fnameE, format='MSEED')
            stZ.write(directory + '/' + fnameZ, format='MSEED')
            with open('../GPDcode/' + filename, 'a') as file:
                file.write(fnameN + ' ' + fnameE + ' ' + fnameZ + '\n')
            print("Downloaded ",fname)
        except:
            print("Download failed for ",fname)
