#----- import modules

import numpy as np
from obspy import read

#----- parameters

infile = 'for_rythym.in'

#----- read list of mseed files

npts_want = 20*10
time_want = 20.
f0 = open(infile)
lines = f0.readlines()
f0.close()
for line in lines:
    words = line.split()
    filenameN = words[0]
    filenameE = words[1]
    filenameZ = words[2]
#    print(filenameN, filenameE, filenameZ)

    stN = read(words[0])
    dt = stN[0].stats.delta
    start = stN[0].stats.starttime
    end = stN[0].stats.starttime + time_want - (dt*1)
    stN.trim(start, end, pad=True, fill_value=0. )
    stN.normalize()
    dataN = stN[0].data

    stE = read(words[0])
    start = stE[0].stats.starttime
    end = stE[0].stats.starttime + time_want - (dt*1)
    stE.trim(start, end, pad=True, fill_value=0. )
    stE.normalize
    dataE = stE[0].data

    stZ = read(words[0])
    start = stZ[0].stats.starttime
    end = stZ[0].stats.starttime + time_want - (dt*1)
    stZ.trim(start, end, pad=True, fill_value=0. )
    stZ.normalize()
    dataZ = stZ[0].data

#    print( type(dataZ), len(dataZ), dataZ[100*10] )

