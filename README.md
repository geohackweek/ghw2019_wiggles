# Seismic wiggle discriminator aka the Amy2000
This is a project developed by team Wiggle from the [2019 Geohack Week](https://geohackweek.github.io/) at the University of Washington. 

The scope of the Wiggle project has two goals. 1) Test and asses the [Generalized Phase Detection](https://github.com/interseismic/generalized-phase-detection) (GDP) algorithm, which was trained on Southern California events, using [Pacific Northwest Seismic Network](https://pnsn.org) (PNSN) event data. 2) Retrain the GDP to discriminate between both P and S-waves from the following event types.  This expands the number of labels from two: P and S, to ten: EQP, EQS, SUP, SUS, etc.
* EQ - Earthquakes: mostly local events, a few regional events
* SU - Surface Events: rockslides, avalanches, etc.  Mostly on volcanoes. 
* PX - Probable explosion: most are quarry blasts. 
* TH - Thunder
* SN - Sonic Shockwave: jets breaking the sound barrier, bolides exploding in the atmosphere...

# Data
Arrival data were querried from arrivals (table: arrival) from the PNSN AQMS database ([schema is in "parametric info"](http://www.ncedc.org/db/)). Pick data were then used to download the waveform data from [IRIS](http://ds.iris.edu/ds).  Only data which were gapless on Vertical, North-South, and East-West components were used.

# Preprocessing

# Contributors
* Jon Connolly joncon@uw.edu
* Bao Tran Do trando46@gmail.com
* Ariane Ducellier ducela@uw.edu
* Alex Hutko ahutko@uw.edu 
* Gabija Pasiunaite gabija.pasiunaite@gmail.com
* Rhythm Shah rhythm_shah99@yahoo.com
* Liang Xue  xlia@okstate.edu


