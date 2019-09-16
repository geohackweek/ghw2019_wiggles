# Seismic wiggle discriminator
This is a project developed by team Wiggle from the [2019 Geohack Week](https://geohackweek.github.io/) at the University of Washington. 

The scope of the Wiggle project has two goals. 1) Test and asses the [Generalized Phase Detection](https://github.com/interseismic/generalized-phase-detection) (GPD) algorithm, which was trained on Southern California events, using [Pacific Northwest Seismic Network](https://pnsn.org) (PNSN) event data. 2) Retrain the GDP to discriminate between both P and S-waves from the following event types.  This expands the number of labels from two: P and S, to ten: EQP, EQS, SUP, SUS, etc.
* EQ - Earthquakes: mostly local events, a few regional events
* SU - Surface Events: rockslides, avalanches, etc.  Mostly on volcanoes. 
* PX - Probable explosion: most are quarry blasts. 
* TH - Thunder
* SN - Sonic Shockwave: jets breaking the sound barrier, bolides exploding in the atmosphere...

# Data
Arrival data were querried from arrivals (table: arrival) from the PNSN AQMS database ([schema is in "parametric info"](http://www.ncedc.org/db/)) and are in the [arrivals.csv](https://github.com/geohackweek/ghw2019_wiggles/blob/master/arrivals.csv) file. Pick data were then used to download the waveform data from [IRIS](http://ds.iris.edu/ds) using [get_waveform_data.py](https://github.com/geohackweek/ghw2019_wiggles/blob/master/get_waveform_data.py).  Only data which were gapless and had 3 components available (Vertical, North-South, and East-West) were used.

# Preprocessing
We chose to use 20 sec long windows centered on the pick arrival to test the GPD algorithm.  We prepared this data by initially downloading 50 sec of data centered on the pick in order to have a 15 sec buffer on each end of the trace so that filtering effects wouldn't affect the analyzed traces.  All data were:
* demeaned
* tapered
* instrument response corrected to velocity using a pre_filt = (0.3, 0.5, 40. 45.)
* highpass filtered above 0.5 Hz
* resampled to 100 Hz sampling
* trimmed to exactly 2000 points (20 sec x 100 sps)
* written to mseed (about 20kb each file)

# Environment setup
To run these codes, make sure you setup an appropriate python environment with the correct modules using the [environment.yml](https://github.com/geohackweek/ghw2019_wiggles/blob/master/environment.yml):
```
conda env create --file environment.yml
conda activate seismic-wiggles-env
```

# Contributors
* [Jon Connolly](https://github.com/joncon)  joncon@uw.edu
* Bao Tran Do  trando46@gmail.com
* Ariane Ducellier  ducela@uw.edu
* [Alex Hutko](https://github.com/alexhutko)  ahutko@uw.edu 
* [Gabija Pasiunaite](https://github.com/pasiunaite)  gabija.pasiunaite@gmail.com
* Rhythm Shah  rhythm_shah99@yahoo.com
* [Liang Xue](https://github.com/droxliang)  xlia@okstate.edu


