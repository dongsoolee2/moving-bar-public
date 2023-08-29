# moving-bar

Nonlinear system (retina) identification during visual motion processing & \
Machine Learning models for neurophysiology data

Dongsoo Lee

Baccus Lab, Stanford University


## 1. Nonlinear system identification

Simultaneous extracellular (MEA) and intracellular (sharp electrode) recording \
and `playback` experiment with moving bar stimuli to compute neuronal contribution
to the output (theoretically identical to "Active Noise Control" methods). 

## 2. Generalized Linear Models (GLM) and Hidden Markov Models (HMM)

Machine Learning models to build predictive models for neural computation
during default status and during manipulation.


### Directory

/moving-bar: project path \
    /data-sort: raw data (+ spike time sorted) \
    /data-extract: extracted data (by using notebook/`01_extract.ipynb`) \
    /data-deepretina: extracted data for CNN model (white noise for 30 mins) \
    /json: .json file for parameters (used by notebook/`01_extract.ipynb`) \
    /manuscript: paper \
    /venv: virtual environment \
    /experiment.py: python class to organize extracted experiment data \
    /extract.py: python functions to extract data and load visual stimuli \
    /utils.py: other functions (h5view, filename, filter, color, plot setting,
    etc.) \
