import sys
import pandas as pd
import numpy as np
import os
import obspy.core as oc

from scipy import stats
import scipy.constants
from obspy import UTCDateTime

import matplotlib.pyplot as plt 
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
from matplotlib.dates import date2num
from matplotlib.lines import Line2D
import datetime


def split(word):
    chars = [char for char in word]
    charsout = []
    for c in chars:
        charsout.append('(' + c + ')')
    return charsout

def build_stream(df,h5,line, wftype, filt, freq_min, freq_max):

    """
    Build the Streams from events data in counts saved in hdf5 files as np.array
    line : integer, line number of the hdf5 File to plot
    wftype : str, waveform type 'ev_c', 'ev_gm' or 'noise' for events in counts, events in ground motion units or noise, respectively
    filt : logical, if you want to apply a bandpass filter to the data
    freq_min and freq_max : minimum and maximum frequency
    
    """
    row = df.iloc[line,:]

    stats = oc.Stats()
    stats.npts = 12000
    stats.sampling_rate = 100.

    sta = row['station_code']
    wav_name = row['trace_name']
    ev_id = row['source_id']
    net = row['station_network_code']
    
    waveform = h5['data'][row['trace_name']]

    stats.delta = row['trace_dt_s']
    stats.starttime = pd.to_datetime(row['trace_start_time'])
    stats.network = net
    stats.station = sta
    
    st = oc.Stream()
    for i in range (0,3):
        tr = oc.Trace()
        tr.data = waveform[i]
        tr.stats = stats
        if i == 0:
            tr.stats.channel = row['file_E'].split('.')[3]
        if i == 1:
            tr.stats.channel = row['file_N'].split('.')[3]
        if i == 2:
            tr.stats.channel = row['file_Z'].split('.')[3]
        tr +=tr
        st.append(tr)        

    latest_start = np.max([x.stats.starttime for x in st])
    earliest_stop = np.min([x.stats.endtime for x in st])
    st.trim(latest_start, earliest_stop)

    if filt == True:
        st.detrend(type='linear')
        st.filter(type='bandpass', freqmin=freq_min, freqmax=freq_max)

    return st,row

def multiple_streams(df,h5,lines,wftype,nrow,ncol,units,labs,filt,freq_min,freq_max):

    """
    Build the multi-panel figure for events in counts
    lines : list of lines, lines number of the hdf5 File to plot
    wftype : str, waveform type 'ev_c', 'ev_gm' or 'noise' for events in counts, events in ground motion units or noise, respectively
    nrow : number of rows in figure
    ncol : numebr of columns in figure
    units : list of units
    labs : list of labels for publication
    filt : logical, if you want to apply a bandpass filter to the data
    freq_min and freq_max : minimum and maximum frequency

    """    
    title_size = 24
    labelsize = 24
    legendsize = 20
    label_sec=range(0,60,30)
    formatter = mdates.DateFormatter("%H:%M:%S")

    (fig_width, fig_height) = plt.rcParams['figure.figsize']
 
    fig_size = [fig_width*2*ncol, fig_height*2*nrow]
    
    fig = plt.figure(figsize=fig_size)
    outer = gridspec.GridSpec(nrow, ncol, wspace=0.4, hspace=0.4)

    irow=3
    for i in range(nrow*ncol):
        inner = gridspec.GridSpecFromSubplotSpec(irow, 1,
                        subplot_spec=outer[i], wspace=0.2, hspace=0.3)

        l=lines[i] 
        unit=units[i]
        lab=labs[i]
        st,row = build_stream(df,h5,l, wftype, filt, freq_min, freq_max)
        ev_id = row['source_id']
        if wftype != 'noise':
            timeP = row['trace_P_arrival_time']
            timeS = row['trace_S_arrival_time']
        
        smax = st.max()
        absmax = max(abs(n) for n in smax)
        yslim = absmax*1.01


        if wftype != 'noise':
            P_date_time_str = timeP
            P_date_time_obj = datetime.datetime.strptime(P_date_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')

            S_date_time_str = timeS
            if timeS != "" :
                S_date_time_obj = datetime.datetime.strptime(S_date_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')

        custom_lines1 = [Line2D([0], [0], color='k', lw=2),Line2D([0], [0], color='b', lw=2),Line2D([0], [0], color='r', lw=2)]
        if wftype != 'noise':
            custom_lines2 = [Line2D([0], [0], color='b', lw=2),Line2D([0], [0], color='r', lw=2)]
        net = st[0].stats.network
        sta = st[0].stats.station
        if wftype != 'noise':
                name = str(ev_id) + '.' + net + '.' + sta +'.'+str(P_date_time_obj.date())
        else:
                name = str(ev_id)


        for j in range(irow):
            ax = plt.Subplot(fig, inner[j])
            ax.xaxis.set_major_formatter(formatter)
            ax.xaxis.set_major_locator(mdates.SecondLocator(bysecond=label_sec))
            ax.set_ylim(-yslim,yslim)
            ax.plot(st[j].times("matplotlib"), st[j].data, c='k', lw=1, label = "Trace")
            ax.yaxis.set_tick_params(labelleft=True, labelsize=labelsize)
            if wftype != 'noise':
                ax.axvline(date2num(P_date_time_obj), c='b', lw=2, label = "Pick_P")
                if timeS != "" :
                    ax.axvline(date2num(S_date_time_obj), c='r', lw=2, label = "Pick_S")
            ax.xaxis.set_tick_params(labelleft=True, labelsize=labelsize)
            ax.set_ylabel(unit,fontsize=labelsize)
            t = ax.yaxis.get_offset_text()
            t.set_size(22)



            if j ==0:
                ch = st[0].stats.channel
                ax.tick_params(labelleft=True, labelbottom=False)
                ax.set_title(name,pad=20,fontsize=title_size)
                ax.text(1, 1.3, lab, transform=ax.transAxes, fontsize=labelsize,ha='right',va='top')
                if wftype != 'noise':
                    ax.legend(custom_lines1,[ch],fontsize=legendsize,bbox_to_anchor=(0.99, 0.96), loc=1, borderaxespad=0.,shadow=True)
            elif j==1:
                ch = st[1].stats.channel
                ax.tick_params(labelleft=True, labelbottom=False)
                if wftype != 'noise':
                    ax.legend(custom_lines1,[ch],fontsize=legendsize,bbox_to_anchor=(0.99, 0.96), loc=1, borderaxespad=0.,shadow=True)
            elif j == 2:
                ch = st[2].stats.channel
                ax.tick_params(labelleft=True, labelbottom=True)
                ax.set_xlabel("Time",fontsize=labelsize)
                if wftype != 'noise':
                    ax.legend(custom_lines1,[ch],fontsize=legendsize,bbox_to_anchor=(0.99, 0.96), loc=1, borderaxespad=0.,shadow=True)

            ax.set_xlim(date2num(st[0].stats.starttime.datetime),date2num(st[0].stats.endtime.datetime))

            fig.add_subplot(ax)

    fig.show()


