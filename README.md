![event](docs/logo_color.png)

[![DOI](https://img.shields.io/badge/doi-10.13127%2Finstance-lightgray?style=flat-square)](https://doi.org/10.13127/instance)
![GitHub all releases](https://img.shields.io/github/downloads/cjunkk/instance/total?color=green&style=flat-square)

## Description
**INSTANCE** is a dataset of seismic waveforms data and associated metadata **suited for analysis based on machine learning**. It includes:
* 54,008 earthquakes for a total of 1,159,249 3-channel waveforms;
* 132,330 3-channel noise waveforms;
* 116 precomputed observable quantities providing information on *station, trace source, path* and *quality*;
* 19 networks;
* 620 seismic stations.


![maps](docs/Ita_epicenter_station.png)
*Earthquakes a) and stations b) of the dataset. Symbols size are proportional to earthquake magnitude and number of arrival phases recorded by stations, respectively*

## Reference
Michelini A., Cianetti S., Gaviano S., Giunchi C., Jozinović D., and Lauciani V., (2021). INSTANCE - The Italian seismic dataset for machine learning, submitted to *Earth System Science Data*, 2021.
INGV Ufficio Dati https://doi.org/10.13127/instance

## Download
To get the full dataset you have to download:

* [Noise metadata (csv, 8 MB)](http://repo.pi.ingv.it/instance/metadata_Instance_noise.csv.bz2)
* [Noise data in counts (hdf5, 3.9 GB)](http://repo.pi.ingv.it/instance/Instance_noise.tar.bz2)

* [Events metadata (csv, 249 MB)](http://repo.pi.ingv.it/instance/metadata_Instance_events.csv.bz2)
* [Events data in counts (hdf5, 39 GB)](http://repo.pi.ingv.it/instance/Instance_events_counts.tar.bz2) **single file**  
Alternatively this file can also be downloaded in smaller size chunks:
  * [Events data in counts (hdf5, 10 GB)](http://repo.pi.ingv.it/instance/Instance_events_counts.tar.bz2.part-a) **part a**
  * [Events data in counts (hdf5, 10 GB)](http://repo.pi.ingv.it/instance/Instance_events_counts.tar.bz2.part-b) **part b**
  * [Events data in counts (hdf5, 10 GB)](http://repo.pi.ingv.it/instance/Instance_events_counts.tar.bz2.part-c) **part c**
  * [Events data in counts (hdf5,  9 GB)](http://repo.pi.ingv.it/instance/Instance_events_counts.tar.bz2.part-d) **part d**

* [Events data in ground motion units (hdf5, 307 GB)](http://repo.pi.ingv.it/instance/Instance_events_gm.tar.bz2) **single file**  
Alternatively this file can also be downloaded in smaller size chunks:
  * [Events data in ground motion units (hdf5, 20 GB)](http://repo.pi.ingv.it/instance/Instance_events_gm.tar.bz2.part-a) **part a**
  * [Events data in ground motion units (hdf5, 20 GB)](http://repo.pi.ingv.it/instance/Instance_events_gm.tar.bz2.part-b) **part b**
  * [Events data in ground motion units (hdf5, 20 GB)](http://repo.pi.ingv.it/instance/Instance_events_gm.tar.bz2.part-c) **part c**   
  * [Events data in ground motion units (hdf5, 20 GB)](http://repo.pi.ingv.it/instance/Instance_events_gm.tar.bz2.part-d) **part d**
  * [Events data in ground motion units (hdf5, 20 GB)](http://repo.pi.ingv.it/instance/Instance_events_gm.tar.bz2.part-e) **part e**
  * [Events data in ground motion units (hdf5, 20 GB)](http://repo.pi.ingv.it/instance/Instance_events_gm.tar.bz2.part-f) **part f**
  * [Events data in ground motion units (hdf5, 20 GB)](http://repo.pi.ingv.it/instance/Instance_events_gm.tar.bz2.part-g) **part g**
  * [Events data in ground motion units (hdf5, 20 GB)](http://repo.pi.ingv.it/instance/Instance_events_gm.tar.bz2.part-h) **part h**
  * [Events data in ground motion units (hdf5, 20 GB)](http://repo.pi.ingv.it/instance/Instance_events_gm.tar.bz2.part-i) **part i**
  * [Events data in ground motion units (hdf5, 20 GB)](http://repo.pi.ingv.it/instance/Instance_events_gm.tar.bz2.part-j) **part j**
  * [Events data in ground motion units (hdf5, 20 GB)](http://repo.pi.ingv.it/instance/Instance_events_gm.tar.bz2.part-k) **part k**
  * [Events data in ground motion units (hdf5, 20 GB)](http://repo.pi.ingv.it/instance/Instance_events_gm.tar.bz2.part-l) **part l**
  * [Events data in ground motion units (hdf5, 20 GB)](http://repo.pi.ingv.it/instance/Instance_events_gm.tar.bz2.part-m) **part m**
  * [Events data in ground motion units (hdf5, 20 GB)](http://repo.pi.ingv.it/instance/Instance_events_gm.tar.bz2.part-n) **part n**
  * [Events data in ground motion units (hdf5, 20 GB)](http://repo.pi.ingv.it/instance/Instance_events_gm.tar.bz2.part-o) **part o**
  * [Events data in ground motion units (hdf5,  7 GB)](http://repo.pi.ingv.it/instance/Instance_events_gm.tar.bz2.part-p) **part p**



The **notebooks** provided in this repo can be used to reproduce the figures of the manuscript Michelini et al., 2021, submitted.

We also distribute a very small size **sample dataset** to run the notebooks provided in the repository. Users potentially interested can evaluate whether **INSTANCE** fulfill their requirements without the cumbersome task of downloading the whole dataset.
* **Sample dataset** (GB) : https://www.pi.ingv.it/instance/sample_dataset


## Requirements
To run the notebooks please make sure the following packages are properly installed in your environments:
* python
* obspy
* matplotlib
* numpy
* basemap
* pandas
* seaborn
* h5py
* hdf5
* scipy

## Licence

Creative commons license [Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/legalcode)
