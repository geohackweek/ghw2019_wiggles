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
# Running the GPD code
```
python gpd_predict.py -P -V -I my_infile -O my_outfile
```
The -P suppresses plotting, -V is for verbose output.  Infiles can be found in the [input_files folder](https://github.com/geohackweek/ghw2019_wiggles/tree/master/input_files) and are generated with [make_in_file.py](https://github.com/geohackweek/ghw2019_wiggles/blob/master/make_in_file.py).  Initially, we have used the default hyperparameters in the gpd_predicty.py file.

Input files look like:
```
DATA/EQP/CC.SIFT.--.BHN.20190910154231.mseed DATA/EQP/CC.SIFT.--.BHE.20190910154231.mseed DATA/EQP/CC.SIFT.--.BHZ.20190910154231.mseed
DATA/EQP/CC.PR05.--.BHN.20190910154231.mseed DATA/EQP/CC.PR05.--.BHE.20190910154231.mseed DATA/EQP/CC.PR05.--.BHZ.20190910154231.mseed
```
Output files look like:
```
CC SIFT P 2019-09-10T15:42:41.380000
CC SIFT S 2019-09-10T15:42:43.580000
CC PR05 P 2019-09-10T15:42:41.020000
CC PR05 S 2019-09-10T15:42:43.020000
```
Example of plot output from gpd_predict.py:

<img src="https://github.com/geohackweek/ghw2019_wiggles/blob/master/example_GPD_figure.png" width=400 alt="Metric: Noise Floor" />

# Analyzing GPD results on data with PNSN picks
[compare.py](https://github.com/geohackweek/ghw2019_wiggles/blob/master/compare.py) is used to read the GPD output and compare with the arrivals.csv file of PNSN picks and tally up results.  Results are in the [comparison_out](https://github.com/geohackweek/ghw2019_wiggles/tree/master/comparison_out) folder.  Note: this was not 100% finished and needs to be hand verified.  [histogram.ipynb](https://github.com/geohackweek/ghw2019_wiggles/blob/master/scripts/histogram.ipynb) in the [scripts](https://github.com/geohackweek/ghw2019_wiggles/blob/master/scripts) folder is a notebook to visualize histograms of all of the results.  Note: this still needs work on details like axis ranges.

Format of ???.arrivals.txt files (info from PNSN database):
```
CC TMBU P 2019-08-16T17:54:40.535540 e THP
CC OBSR P 2019-08-10T07:17:45.080000 e THP
CC JRO P 2019-08-10T06:39:49.349630 i THP
```
Columns:
net, station, P or S wave, time of arrival*, quality (e=emergent, i=impulsive), label
Note: time of arrival is true time and does not take into account leap seconds, so they are ahead of unix time (used by the IRIS data center where data are downloaded from) by up to 27 seconds (as of 2019). [Leap Seconds @wikipedia](https://en.wikipedia.org/wiki/Leap_second)

Format of the comp.???.out files:
```
PXP P -0.108350
PXP N nan
PXP P 7.992490 -0.007510 -2.607510
PXP P 0.193560
```
Columns:
1) the etype and phase label from PNSN database
2) the prediction from GPD: P, S.  N = no pick in the window was made.
3) the difference in time(s) between the picked arrival (at 10 sec into 20 sec seisogram) and the time of the GPD pick(s)
*need to make sure that if say a PXP goes in and there are predictions for both P and S waves, that it is properly accounted for

*Next steps:
The initial database queries were blind to source characteristics beyond etype (EQ, SU), i.e. depth and magnitude were ignored, and were sorted from latest to earliest.  A proper test would be to split data into shallow and deep events and just focus on earthquakes at first.  Also useful would be to bin results according to distance and include local, regional and teleseismic signals.  Finally, there are a few hyperparemeters such as filter corners to consider.*

# Making a new model to expand labels beyond P & S waves from earthquakes
[WiggleNet.ipynb](https://github.com/geohackweek/ghw2019_wiggles/blob/master/WiggleNet.ipynb) is a notebook that has the skeleton framework to generate a new model to expand the labels to include P and S waves from other event types, e.g. surface events/avalances (SU), probably quarry blasts (PX), etc.
Where one *could* go with this:
* expand labels to include multiple different event types
* explore using different length time windows to apply the final model to, e.g. use only 1, 5, 10 sec...
* count lightning strike effects (currently not labeled)
* surface events (e.g. avalanches) may require longer time windows to correctly discriminate, i.e. explore different length windows' accuracy for different event types

# Contributors
* [Jon Connolly](https://github.com/joncon)  joncon@uw.edu
* Bao Tran Do  trando46@gmail.com
* Ariane Ducellier  ducela@uw.edu
* [Alex Hutko](https://github.com/alexhutko)  ahutko@uw.edu 
* [Gabija Pasiunaite](https://github.com/pasiunaite)  gabija.pasiunaite@gmail.com
* Rhythm Shah  rhythm_shah99@yahoo.com
* [Liang Xue](https://github.com/droxliang)  xlia@okstate.edu

# Internal notes and updates to team Wiggles
* [Link to private slack channel](https://app.slack.com/client/TG1K11UCV/CN75TD4V6)
* .mseed files (about 20kb each) are in /srv/shared/wiggles/
* .mseed file names have been updated and reflect the correct starttime

