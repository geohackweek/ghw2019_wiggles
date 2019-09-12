
import glob
outdir = '/srv/shared/wiggles'
for etype in ['EQS','EQP','SUS','SUP','THS','THP','SNS','SNP','PXS','PXP']:
    outfile = 'mseedfiles.' + etype + ".in"
    f0 = open(outfile,'w')
    mseedlist = glob.glob(outdir + "/" + etype + "/" + "*N.201*mseed" )
    for mseedN in mseedlist:
        chanN = "." + mseedN.split('.')[3] + "." 
        chanZ = chanN[0:3] + "Z."
        chanE = chanN[0:3] + "E."
        mseedZ = mseedN.replace(chanN, chanZ)
        mseedE = mseedN.replace(chanN, chanE)
        print(mseedN, mseedE, mseedZ)
        outstring = mseedN + " " + mseedE + " " + mseedZ + "\n"
        f0.write(outstring)
    f0.close()


