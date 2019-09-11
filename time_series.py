
import obspy

#----- trim traces to common start and end times.  Npoints are
#      forced to be the same.  Assumes only 1 trace per stream.
#      Performed in-place.

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


#----- If data are not the right sample rate, resmaple it.  If you need to
#      downsample, first try decimation (faster) otherwise use resample.
#      If you need to upsample, use interpolate.

def correct_sample_rate(st, sample_rate):
    if ( st[0].stats.sampling_rate > sample_rate ):
        factor = st[0].stats.sampling_rate / sample_rate
        factor_mod = st[0].stats.sampling_rate % sample_rate
        if ( factor_mod == 0 ):
            st.decimate(factor)
        else:
            st.interpolate(sampling_rate = sample_rate)
    else:
        st.interpolate(sampling_rate = sample_rate)

    return st

