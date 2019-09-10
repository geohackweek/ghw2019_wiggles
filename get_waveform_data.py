#!/home/ahutko/anaconda3/bin/python

import psycopg2
import obspy
from obspy import UTCDateTime
from obspy.clients.fdsn import Client

#--------- parameters to modify ----------
client = Client("IRIS")
eqtime = UTCDateTime("2019-07-12T09:51:38")
label = "Monroe_M4.6"
TBeforeArrival = 90.
TAfterArrival = 90.
common_sample_rate = 100.  # in Hz
#-----------------------------------------

f0 = open(label + ".in",'w')
f1 = open(label + ".out.database",'w')

#--------- get picks from PNSN database -------------
# https://internal.pnsn.org/LOCAL/WikiDocs/index.php/Accessing_the_AQMS_databases

#arrival table:
#rflag: H = human, A = automatic, F = finalized
#archdb=> select * from arrival limit 10;
#   arid   | commid |     datetime     | sta  | net | auth | subsource | channel | channelsrc | seedchan | location | iphase | qual | clockqual | clockcorr | ccset | fm | ema | azimuth | slow | deltim | d
#elinc | delaz | delslo | quality | snr | rflag |       lddate        
#----------+--------+------------------+------+-----+------+-----------+---------+------------+----------+----------+--------+------+-----------+-----------+-------+----+-----+---------+------+--------+--
#------+-------+--------+---------+-----+-------+---------------------
# 10576803 |        | 1329276740.71738 | KEB  | NC  | UW   | Jiggle    |         |            | HHZ      |          | P      | i    |           |           |       | d. |     |         |      |   0.06 |      |       |        |     0.8 |     | H     | 2012-03-12 18:33:05
# 10576808 |        |  1329276770.3577 | KEB  | NC  | UW   | Jiggle    |         |            | HHN      |          | S      | e    |           |           |       | .. |     |         |      |    0.3 |      |       |        |     0.3 |     | H     | 2012-03-12 18:33:05
# 10576813 |        | 1329276742.40491 | TAKO | UW  | UW   | Jiggle    |         |            | BHZ      |          | P      | i    |           |           |       | c. |     |         |      |   0.06 |      |       |        |     0.8 |     | H     | 2012-03-12 18:33:05
# 10576818 |        | 1329276774.06588 | TAKO | UW  | UW   | Jiggle    |         |            | BHE      |          | S      | e    |           |           |       | .. |     |         |      |   0.15 |       |       |        |     0.5 |     | H     | 2012-03-12 18:33:05

#----- Connect to database

dbname = '#####'
dbuser = '#####'
hostname = '#####'   # check if pp1 or pp2 is the current sarchdb
dbpass = '#####'

conn = psycopg2.connect(dbname=dbname, user=dbuser, host=hostname, password=dbpass)
cursor = conn.cursor()

#----- From database, get all arrivals within a small time window

epoch0time = UTCDateTime("1970-01-01T00:00:00")
eqepoch1 = eqtime - epoch0time - 5
eqepoch2 = eqtime - epoch0time + 90

#cursor.execute('INSERT INTO metrics (metric,unit,description,created_at,updated_at) VALUES (%s, %s, %s, %s, %s)', (metric,unit,description,now,now) )
#        cursor.execute('UPDATE scnls SET nslc = (%s) WHERE net = (%s) AND sta = (%s) AND loc = (%s) AND chan = (%s)',(sncl, net, sta, loc, chan))

cursor.execute('select * from arrival where datetime > (%s) and datetime < (%s) ;', (eqepoch1, eqepoch2) )

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
        T1 = ut - TAfterArrival
        T2 = ut + TBeforeArrival
        minlen = T2 - T1 - 1
        minlen = 1
        strdate = str(T1.year) + str(T1.month).zfill(2) + str(T1.day).zfill(2) + \
                  str(T1.hour).zfill(2) + str(T1.minute).zfill(2) + \
                  str(T1.second).zfill(2)
        fname = sncl + "." + strdate + ".mseed"
        try:
            chan = chan[:2] + "N"
            fnameN = netstatloc + "." + chan + "." + strdate + ".mseed"
            st = client.get_waveforms(network=net, station=stat, location=loc, 
                                      channel=chan, starttime=T1, endtime=T2, 
                                      minimumlength = minlen, longestonly = True,
                                      filename = fnameN )
            chan = chan[:2] + "E"
            fnameE = netstatloc + "." + chan + "." + strdate + ".mseed"
            st = client.get_waveforms(network=net, station=stat, location=loc, 
                                      channel=chan, starttime=T1, endtime=T2, 
                                      minimumlength = minlen, longestonly = True,
                                      filename = fnameE )
            chan = chan[:2] + "Z"
            fnameZ = netstatloc + "." + chan + "." + strdate + ".mseed"
            st = client.get_waveforms(network=net, station=stat, location=loc, 
                                      channel=chan, starttime=T1, endtime=T2, 
                                      minimumlength = minlen, longestonly = True,
                                      filename = fnameZ )
            #----- make sure it's the correct sampling rate
            if ( st[0].stats.sampling_rate > common_sample_rate ):
                factor = st[0].stats.sampling_rate / common_sample_rate
                factor_mod = st[0].stats.sampling_rate % common_sample_rate
            if ( factor_mod == 0 ):
                st.decimate(factor)
            else:
                st.interpolate(sampling_rate = common_sample_rate)
            #----- write out the data to an .mseed file

            f0.write( str(fnameN) + " " + str(fnameE) + " " + str(fnameZ) + '\n' )
            f1.write( net + " " + stat + " " + phase + " " + str(ut)[:-1] + " " + str(qual) + '\n' )  # AZ TRO P 2016-06-10T00:03:53.808300
            print("Downloaded ",fname)
        except:
            print("Download failed for ",fname)

f0.close()
f1.close()

