import sys
import pandas as pd
import numpy as np
import os

from scipy import stats
import scipy.constants
from obspy import UTCDateTime

import seaborn as sns
import matplotlib.pyplot as plt 
import matplotlib.ticker as ticker



sns.set(rc={'figure.figsize':(11.7,8.27)})

def split(word):
    chars = [char for char in word]
    charsout = []
    for c in chars:
        charsout.append('(' + c + ')')
    return charsout


def detect_time(time_string):
    try:
        b = UTCDateTime(time_string)
        return b
    except:
        return np.nan
    
def bin_width(rangemin,rangemax,width):
    bin_edges = []
    nbins = round((rangemax - rangemin)/width)
    for i in range(nbins+1):
        b1 = rangemin - width/2. + i*width
        bin_edges.append(b1)  
    return np.array(bin_edges)

def my_ceil(a, precision=0):
    return np.round(a + 0.5 * 10**(-precision), precision)

def my_floor(a, precision=0):
    return np.round(a - 0.5 * 10**(-precision), precision)

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def plot_subplot(se,idx,title,xlabel,ylabel,axes):
    se.plot(ax=axes[idx])
    axes[idx].set_title(title);
    # axes[idx].set_xlim(0, maxval)
    axes[idx].set_xlabel(xlabel)
    axes[idx].set_ylabel(ylabel)
    axes[idx].grid(True)
    
    
def hist_subplot(se,idx,title,xlabel,ylabel,axes,nbins):
    se.hist(ax=axes[idx],bins=nbins, log=True)
    axes[idx].set_title(title);
    # axes[idx].set_xlim(0, maxval)
    axes[idx].set_xlabel(xlabel)
    axes[idx].set_ylabel(ylabel)
    axes[idx].grid(True)
    

####################
#### HEXBIN PLOTS

def plot_hexbin_panels(style_label,df,cols,ncols,nrows,label_font_size,tick_label_font_size,labs,colors,
                       logs,ranges,bins, **kwargs):
    
    """
    Multiple Hexbin plots 
    
    style_label: string
                 seaborn style label. Options:
                     'seaborn-deep'
                     'default'
                     'seaborn-darkgrid'
    
    df: dataframe of metadata
    
    cols: array of subarrays of strings
          The 2 elements of each subarray represent the fields of the dataframe to be represented on the x and y axes,
          respectively
          
    ncols: integer
        Number of columns of the subplot
    
    nrows: integer
           Number of rows of the subplot
        
    label_font_size: array of floats
                 font size of the labels of the x and y axes
    
    tick_label_font_size: array of floats
                 font size of the ticks of the x and y axes   
    
    labs: array of chars
          The length of the arrey is equal to the number of subplots. It contains the letters to label the subplots  
    
    colors: array of chars
    
    logs: array of subarrays of booleans
          Set the logscale for the x and y axes for each subplot
    
    ranges: array of subarrays of floats.
            Each subarray represents the limits of the axes for each subplot.
            The subarray dimension can be 2 or 4 whatever are defined only the xlimit or both the xlimits and ylimits 
    
    bins: array.
          For each subplot is a parameter for the discretization of the hexagon values.
          Each value can be 'log' or an integer.
          Look at the hexbin function definition of matplotlib - parameter 'bins'- for more details
    
    
    ** kwargs:
        
        ylabel_text: array of strings
                     list of the labels of the y axes of the suplots ( if you want to set them manually) 
        
        n_x_ticks:  integer, optional
                    number of ticks on the x axis
        
        n_y_ticks:  integer, optional
                    number of ticks on the y axis
    
    """

    if 'ylabel_text' in kwargs:
        ylabel_text = kwargs.pop('ylabel_text')
    
    if 'n_x_ticks' in kwargs:
        n_x_ticks=kwargs.pop('n_x_ticks')

    if 'n_y_ticks' in kwargs:
        n_y_ticks=kwargs.pop('n_y_ticks')
    
    
    for key, value in kwargs.items():
        print(key, value)
    
    with plt.style.context(style_label):
        (fig_width, fig_height) = plt.rcParams['figure.figsize']
        #
        if (nrows == 1) and (ncols == 1):
            fig_size = [fig_width, fig_height]
        elif (nrows == 1) and (ncols > 1):
            fig_size = [fig_width * 2, fig_height]
        elif (nrows > 1) and (ncols == 1):
            fig_size = [fig_width, fig_height*2]
        elif (nrows == 2)  and (ncols > 1):
            fig_size = [fig_width*2, fig_height*1.5]
        else:
            fig_size = [fig_width*2, fig_height*2]

        fig, axes = plt.subplots(ncols=ncols, nrows=nrows, num=style_label,
                                 figsize=fig_size, squeeze=True)
        
        if len(cols) > 1:
#             print (axes.shape)
            axes = axes.flatten()
#             axes = axes.T.flatten()
#             print (axes.shape)
            for i in range(len(cols)):

                if logs[i][0]:
#                     axes[i].set_xscale('log')
                    xlinlog = 'log'
                #
                #find min value
                    min_x = np.nanmin(df[cols[i][0]].values)
                    ranges[i][0] = min_x
                    ranges[i][:2] = np.log10(ranges[i][:2])
                else:
#                     axes[i].set_xscale('linear')
                    xlinlog = 'linear'
                
                if logs[i][1]:
#                     axes[i].set_yscale('log')
                    ylinlog = 'log'
                    min_y = np.nanmin(df[cols[i][1]].values)
                    ranges[i][2] = min_y
                    ranges[i][2:] = np.log10(ranges[i][2:])
                        
                else:
#                     axes[i].set_yscale('linear')
                    ylinlog = 'linear'
                
                print (ranges[i])

                cs = axes[i].hexbin(df[cols[i][0]].values,df[cols[i][1]].values, 
                                    bins=bins[i],extent=ranges[i], xscale=xlinlog, yscale=ylinlog, **kwargs)

                # set font size of the labels
                axes[i].set_xlabel(cols[i][0],fontsize=label_font_size[i])
                
                try:
                    axes[i].set_ylabel(ylabel_text[i],fontsize=label_font_size[i])
                except:                  
                    axes[i].set_ylabel(cols[i][1],fontsize=label_font_size[i])
                #
                # add the label of the figure number
                axes[i].text(0.95, 0.95, labs[i], transform=axes[i].transAxes, ha='right',va='top',fontsize=30,c='w')
                #
                # set font size of the tickmark labels
                for tick in axes[i].xaxis.get_major_ticks():
                    tick.label.set_fontsize(tick_label_font_size[i])
                for tick in axes[i].yaxis.get_major_ticks():
                    tick.label.set_fontsize(tick_label_font_size[i])
                cb=fig.colorbar(cs, ax=axes[i])
                
                for t in cb.ax.get_yticklabels():
                     t.set_fontsize(tick_label_font_size[i])
                
                # Define the number of ticks on the x axis
                try:
                    if len(n_x_ticks)==1 :
                        axes[i].locator_params(axis='x', nbins=n_x_ticks)
                    elif len(n_x_ticks)>1:
                        axes[i].locator_params(axis='x', nbins=n_x_ticks[i])
                except:
                    pass
                
                if logs[i]==False:   # If the y axis is not logaritmic
                    try:
                        if len(n_y_ticks)==1 :
                            axes[i].locator_params(axis='y', nbins=n_y_ticks)
                        elif len(n_y_ticks)>1:
                            axes[i].locator_params(axis='y', nbins=n_y_ticks[i])  
                    except:
                        pass
                #### LOGARITMIC SCALE SET ON THE Y AXIS: Define the number of ticks  ###
                else:                        
                    try:    
                        if len(n_y_ticks)==1:
                            axes[i].yaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=n_y_ticks))
                        elif len(n_y_ticks)>1:
                            axes[i].yaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=n_y_ticks[i]))    
                    except:
                        pass
                        

        else:
            if logs[0][0]:
#                 axes.set_xscale('log')
                xlinlog = 'log'
            #
            #find min value
                min_x = np.nanmin(df[cols[i][0]].values)
                ranges[0][0] = min_x
                ranges[i][:2] = np.log10(ranges[i][:2])
            else:
#                 axes.set_xscale('linear')
                xlinlog = 'linear'

            if logs[0][1]:
#                 axes.set_yscale('log')
                ylinlog = 'log'
                min_y = np.nanmin(df[cols[i][1]].values)
                ranges[0][2] = min_y
                ranges[0][2:] = np.log10(ranges[i][2:])

            else:
#                 axes.set_yscale('linear')
                ylinlog = 'linear'


#             plot_scatter(axes, df[cols[0][0]].values,df[cols[0][1]].values)
            cs = axes.hexbin(df[cols[0][0]].values,df[cols[0][1]].values, bins=bins[0], extent=ranges[0],
                            xscale=xlinlog, yscale=ylinlog, **kwargs)
            #
            if logs[0][0]:
                axes.set_xscale('log')
            else:
                axes.set_xscale('linear')

            if logs[0][1]:
                axes.set_yscale('log')
            else:
                axes.set_yscale('linear')
            #
#             axes.set_xlim(ranges[0][:2])
#             axes.set_ylim(ranges[0][2:])


            # set font size of the labels
            axes.set_xlabel(cols[0][0],fontsize=label_font_size[0])
            axes.set_ylabel(cols[0][1],fontsize=label_font_size[0])
            #
            # set font size of the tickmark labels
            for tick in axes.xaxis.get_major_ticks():
                tick.label.set_fontsize(tick_label_font_size[0])
            for tick in axes.yaxis.get_major_ticks():
                tick.label.set_fontsize(tick_label_font_size[0])
            cb=fig.colorbar(cs, ax=axes)
            
            for t in cb.ax.get_yticklabels():
                t.set_fontsize(tick_label_font_size[0])
            
        fig.tight_layout()
        return fig
    
###############
## 

def plot_histogram(ax,values,bins,colors='r',log=False,xminmax=None):
    """
    plot 1 histogram
    """
    #print (type(values))
    ax.hist(values, histtype="bar", bins=bins,color=colors,log=log,
                alpha=0.8, density=False, range=xminmax)
    # Add a small annotation.
#     ax.annotate('Annotation', xy=(0.25, 4.25),
#                 xytext=(0.9, 0.9), textcoords=ax.transAxes,
#                 va="top", ha="right",
#                 bbox=dict(boxstyle="round", alpha=0.2),
#                 arrowprops=dict(
#                           arrowstyle="->",
#                           connectionstyle="angle,angleA=-95,angleB=35,rad=10"),
#                 )
    return ax


def plot_histo_panels(style_label,df,cols,ncols,nrows,bins,ylabel_text,label_font_size,tick_label_font_size,labs, colors,logs,ranges, **kwargs):
    """
    Plot multiple histograms
    
    style_label: string
               seaborn style label. Options:
                 'seaborn-deep'
                 'default'
                 'seaborn-darkgrid'

    df: dataframe of metadata
    
    cols: array of subarrays of strings
          The 2 elements of each subarray represent the fields of the dataframe to be represented on the x and y axes,
          respectively
          
    ncols: integer
        Number of columns of the subplot
    
    nrows: integer
           Number of rows of the subplot
           
    bins: array of integers
          Each integer the number of equal-width bins in the range. 
          For more details look at the matplotlib histogram description page
    
    ylabel_text: array of strings
                Specify the labels of the y-axes of the different subplots
            
    label_font_size: array of floats
                 font size of the labels of the x and y axes
    
    tick_label_font_size: array of floats
                 font size of the ticks of the x and y axes   
    
    labs: array of chars
          The length of the arrey is equal to the number of subplots. It contains the letters to label the subplots  
    
    colors: array of chars
    
    logs: array of subarrays of booleans
          Set the logscale for the x and y axes for each subplot
    
    ranges: array of subarrays of floats.
            Each subarray represents the limits of the axes for each subplot.
            The subarray dimension can be 2 or 4 whatever are defined only the xlimit or both the xlimits and ylimits 
    
    
    ** kwargs:
    
    n_x_ticks: integer or array of integers
               For each subplot represents the number of ticks of the x-axis 
               
    n_y_ticks: integer or array of integers
                For each subplot represents the number of ticks of the y-axis
    
    bottom: float
            The position of the bottom edge of the subplots, as a fraction of the figure height.
    
    top: float
         The position of the top edge of the subplots, as a fraction of the figure height. 
    
    x_label_text
    
    x_conv: array of floats
            For the multiple subplots. Convertion factor for each x-axes (example: x_cov[i]= 1000 express the km in m) 
    m: integer
       Use it only with the x_conv. Power of 10 of the ticks in the x-axis. Ex: 1 x 10^3 = 1*10^ m
    
    scientific_x: array of booleans
                  For the multiple subplots defines which x-axes express in a scientific notation 
    
    
    """  
    
    
    with plt.style.context(style_label):
        
        (fig_width, fig_height) = plt.rcParams['figure.figsize']
        #
        if (nrows == 1) and (ncols == 1):
            fig_size = [fig_width, fig_height]
        elif (nrows == 1) and (ncols > 1):
            fig_size = [fig_width * 2, fig_height]
        elif (nrows > 1) and (ncols == 1):
            fig_size = [fig_width, fig_height*2]
        elif (nrows == 2)  and (ncols > 1):
            fig_size = [fig_width*2, fig_height*1.5]
        else:
            fig_size = [fig_width*2, fig_height*2]
            
        scientific=False   # Later this variable is set True if 'scientific_x' is in the kwargs

        fig, axes = plt.subplots(ncols=ncols, nrows=nrows, num=style_label,
                                 figsize=fig_size, squeeze=True)
        
        if 'bottom' in kwargs:
            plt.subplots_adjust(bottom = kwargs.pop('bottom'))
        if 'top' in kwargs:
            plt.subplots_adjust(top= kwargs.pop('top'))
        
        if 'xlabel_text' in kwargs:
            xlabel_text=kwargs.pop('xlabel_text')
            
        if 'x_conv' in kwargs:
            x_converter=kwargs.pop('x_conv')
            
        if 'scientific_x' in kwargs:
            scientific=True
            scientific_x=kwargs.pop('scientific_x')    
            m=kwargs.pop('m')
        
        if 'labelpad' in kwargs:
            labelpad=kwargs.pop('labelpad')
        else:
            labelpad=0
            
        if 'n_x_ticks' in kwargs:
            n_x_ticks=kwargs.pop('n_x_ticks')

        if 'n_y_ticks' in kwargs:
            n_y_ticks=kwargs.pop('n_y_ticks')
            

        if len(cols) > 1:
            #print (axes.shape)
            axes = axes.flatten()
#             axes = axes.T.flatten()
            #print (axes.shape)
            for i in range(len(cols)):
                #print (i,cols[i],colors[i])
                try:
                    plot_histogram(axes[i], df[cols[i]].values*x_converter[i],bins[i],colors[i],logs[i],ranges[i][0:2])
                except:
                    plot_histogram(axes[i], df[cols[i]].values,bins[i],colors[i],logs[i],ranges[i][0:2])
                

                
                # Nel caso in cui le tick_labels abbiano una notazione 1e7 permette di applicare la font-size
                axes[i].xaxis.get_offset_text().set_fontsize(tick_label_font_size[i])
                axes[i].yaxis.get_offset_text().set_fontsize(tick_label_font_size[i])                
                
                # Definisci il numero di ticks nell'asse x
                try:
                    if len(n_x_ticks)==1 :
                        axes[i].locator_params(axis='x', nbins=n_x_ticks)
                    elif len(n_x_ticks)>1:
                        axes[i].locator_params(axis='x', nbins=n_x_ticks[i])
                except:
                    pass
                
                if logs[i]==False:   # se l'asse y non è logaritmico
                    try:
                        if len(n_y_ticks)==1 :
                            axes[i].locator_params(axis='y', nbins=n_y_ticks)
                        elif len(n_y_ticks)>1:
                            axes[i].locator_params(axis='y', nbins=n_y_ticks[i])     
                    except:
                        pass
                #### CONDIZIONE SCALA n. TICKS PER SCALA LOGARITMICA SETTATA SOLO PER L'ASSE Y ###
                else:                        
                    try:    
                        if len(n_y_ticks)==1:
                            axes[i].yaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=n_y_ticks))
                        elif len(n_y_ticks)>1:
                            axes[i].yaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=n_y_ticks[i]))    
                    except:
                        pass
                           
                if len(ranges[i])>2:
                    axes[i].set_ylim(ranges[i][2:])
                                                
                #
                # set font size of the labels
                try:
                    axes[i].set_xlabel(xlabel_text[i],fontsize=label_font_size[i], labelpad=labelpad)
                except:
                    axes[i].set_xlabel(cols[i],fontsize=label_font_size[i], labelpad=labelpad)
                    
                axes[i].set_ylabel(ylabel_text[i],fontsize=label_font_size[i])
                #
                axes[i].text(0.97, 0.97, labs[i], transform=axes[i].transAxes, ha='right',va='top', **kwargs)
                #
                # set font size of the tickmark labels
                for tick in axes[i].xaxis.get_major_ticks():
                    tick.label.set_fontsize(tick_label_font_size[i])
                for tick in axes[i].yaxis.get_major_ticks():
                    tick.label.set_fontsize(tick_label_font_size[i])
                    
                for tick in axes[i].xaxis.get_minor_ticks():
                    tick.label.set_fontsize(tick_label_font_size[i])                    
                for tick in axes[i].yaxis.get_minor_ticks():
                    tick.label.set_fontsize(tick_label_font_size[i])
                    
                    
                axes[i].ticklabel_format(axis="x", useMathText=True)
                axes[i].xaxis.major.formatter._useMathText = True
                
                
                if scientific==True and scientific_x[i]==True:
                    axes[i].ticklabel_format(axis="x", style="sci", scilimits=(m,m))                    
            

                    
                    
        else:
            plot_histogram(axes, df[cols[0]].values,bins[0],colors[0],logs[0],ranges[0])
            #
            # set font size of the labels
            axes.set_xlabel(cols[0],fontsize=label_font_size[0])
            axes.set_ylabel(ylabel_text[0],fontsize=label_font_size[0])
            #
            # set font size of the tickmark labels
            for tick in axes.xaxis.get_major_ticks():
                tick.label.set_fontsize(tick_label_font_size[0])
            for tick in axes.yaxis.get_major_ticks():
                tick.label.set_fontsize(tick_label_font_size[0])
                
            for tick in axes.xaxis.get_minor_ticks():
                tick.label.set_fontsize(tick_label_font_size[0])                    
            for tick in axes.yaxis.get_minor_ticks():
                tick.label.set_fontsize(tick_label_font_size[0])
                
                
             # Define the number of ticks of the x-axis
            try:
                axes[i].locator_params(axis='x', nbins=n_x_ticks)
            except:
                pass

            if logs==False:   # If the y-axis in not a logaritmic scale
                try:
                    axes[i].locator_params(axis='y', nbins=n_y_ticks)
                except:
                    pass
            #### Y-Log scale -> number of ticks condition ###
            else:                        
                try:    
                    axes[i].yaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=n_y_ticks))  
                except:
                    pass
                    
                
            axes.xaxis.get_offset_text().set_fontsize(tick_label_font_size[0])
            axes.yaxis.get_offset_text().set_fontsize(tick_label_font_size[0])
                

        fig.tight_layout()
        return fig

    
##############
## PLOT PIES

def plot_pie_panels(df_grouped, cols, ncols, nrows, label_font_size, tick_font_size, **kwargs):
    """
    Plot multiple pie plots
    
    df_grouped: groupby data to be represented in the pie subplots
    
    cols: array of strings
          Titles of the legends of the subplots
    
    cols: integer
        Number of columns of the subplot
    
    nrows: integer
           Number of rows of the subplot
        
    label_font_size: array of floats
                 font size of the labels of the x and y axes
    
    tick_font_size: array of floats
                 font size of the ticks of the x and y axes   
                    
    
    ** kwargs :
    
    wspace : float, optional. 
            The width of the padding between subplots, as a fraction of the average Axes width.
    
    left : float, optional
           The position of the left edge of the subplots, as a fraction of the figure width.
    
    top : float, optional
          The position of the top edge of the subplots, as a fraction of the figure height.
    
    PercMIN : array of floats, optionalPlot_Functions.py
              The length of the array is the number of the subplots. For the legend of each subplot it 
              represents the threshold below which the voice elements is grouped into the single label 'Others'
              
    labs: array of chars
            The length of the arrey is equal to the number of subplots. It contains the letters to label the subplots  
            
    c : char
        color of the letters for the numeration of the subplots
    
    fontsize: float  
           fontsize of the letters for the numeration of the subplots
    
    """

    (fig_width, fig_height) = plt.rcParams['figure.figsize']
    #
    if (nrows == 1) and (ncols == 1):
        fig_size = [fig_width, fig_height]
    elif (nrows == 1) and (ncols > 1):
        fig_size = [fig_width * 2, fig_height]
    elif (nrows > 1) and (ncols == 1):
        fig_size = [fig_width, fig_height*2]
    elif (nrows == 2)  and (ncols > 1):
        fig_size = [fig_width*1.5, fig_height*1.5]
    else:
        fig_size = [fig_width*2, fig_height*2]


    # Make figure and axes
    fig, axs = plt.subplots(nrows, ncols, figsize=fig_size)
    
    if 'wspace' in kwargs:
        plt.subplots_adjust(wspace = kwargs.pop('wspace'))
    if 'left' in kwargs:
        plt.subplots_adjust(left = kwargs.pop('left'))
    if 'top' in kwargs:
        plt.subplots_adjust(top = kwargs.pop('top'))
    if 'PercMIN' in kwargs:
        PercMIN = kwargs.pop('PercMIN')
    try:
        labs = kwargs.pop('labs')
    except:
        pass
    
    cmap = plt.get_cmap("inferno")    
    outer_colors=cmap([50, 255, 140, 90, 115, 0, 170, 200, 220])

    ind=0

    if (len(cols) > 1):
        axs = axs.flatten()

        for i in range(len(cols)):

            ###################
            # GROUP OTHERS
            
            # A standard pie plot
            labels = df_grouped[i].index.values
#
            fracs = df_grouped[i].source_id.values
            fracs = fracs/fracs.sum() * 100
            
            # Labels and fractions in descending order
            labels=[x for _,x in sorted(zip(fracs,labels), reverse=True)]
            fracs.sort()
            fracs=fracs[::-1]   
            
            #print (labels,fracs)
            #[print(l,f) for l,f in zip(labels,fracs) ]
            
            # GROUP in OTHERS IF fracs < MinPerc
            try:
                m_perc=PercMIN[i]
                indici=[]
                for j,perc in enumerate(fracs):
                    if perc< m_perc:
                        indici.append(j)

                if len(indici)>0:
                    oth=0
                    for el in reversed(indici):        
                        oth+=fracs[el]
                        fracs=np.delete(fracs, el)        
                        labels=np.delete(labels,el)

                    labels=np.append(labels,'Others')
                    fracs=np.append(fracs,oth)
            except:
                pass
            
            #print (labels,fracs)
    #         # Adapt radius and text size for a smaller pie

          
            patches, texts, autotexts = axs[i].pie(fracs, labels=labels,
                                                      colors=outer_colors,
                                                      autopct='%.1f%%',
                                                      textprops={'fontsize': 0},
                                                      shadow=False, radius=1.2, labeldistance=None)   
            # Make percent texts even smaller
            for k in range(len(labels)):
                plt.setp(autotexts, size=0)
                autotexts[k].set_color('white')
                
            labels2=[ l+'  '+autotexts[i]._text[:-1]+' %' for i,l in enumerate(labels)]
            
            for indice,perc in enumerate(fracs):
                if perc<1:
                    labels2[indice]= labels[indice]+'  '+'{:.1g}'.format(perc)+' %'
                    
            if labels[-1]=='Others' :
                labels2[-1]=labels[-1]+'  '+'{:.1g}'.format(oth)+' %'
            
            n=len(axs)
            if n>2 and i>=n-2: 
                legend=axs[i].legend(patches, labels2, title=cols[ind], loc="lower left", bbox_to_anchor=(1.1, 0.0, 0.5, 1.0), fontsize=tick_font_size[i])
                legend.get_title().set_fontsize(label_font_size[i])
            else:
                legend=axs[i].legend(patches, labels2, title=cols[ind], loc="upper left", bbox_to_anchor=(1.1, 0.0, 0.5, 1.0), fontsize=tick_font_size[i])
                legend.get_title().set_fontsize(label_font_size[i])
            
            try:
                axs[i].text(0.97, 0.97, labs[i], transform=axs[i].transAxes, ha='right',va='top', **kwargs)
            except:
                pass
            
            ind = ind +1


    else:
        # A standard pie plot
        labels = df_grouped[0].index.values

        fracs = df_grouped[0].source_id.values
        fracs = fracs/fracs.sum() * 100
        
        # Labels and fractions in descending order
        labels=[x for _,x in sorted(zip(fracs,labels), reverse=True)]
        fracs.sort()
        fracs=fracs[::-1]   

        #print (labels,fracs)
        [print(l,f) for l,f in zip(labels,fracs) ]
        
        # GROUP in OTHERS IF fracs < MinPerc
        try:
            m_perc=PercMIN
            indici=[]
            for j,perc in enumerate(fracs):
                if perc< m_perc:
                    indici.append(j)

            if len(indici)>0:
                oth=0
                for el in reversed(indici):        
                    oth+=fracs[el]
                    fracs=np.delete(fracs, el)        
                    labels=np.delete(labels,el)

                labels=np.append(labels,'Others')
                fracs=np.append(fracs,oth)
        except:
            pass

        
        patches, texts, autotexts = axs.pie(fracs, labels=labels,
                                                  colors=outer_colors,
                                                  autopct='%.f%%',
                                                  textprops={'size': 'smaller'},
                                                  shadow=False, radius=1.2, labeldistance=None)
    #     # Make percent texts even smaller
    #     for k in range(len(labels)):
    #         plt.setp(autotexts, size='x-small')
    #         autotexts.set_color('white')

        legend=axs.legend(patches, labels, title=cols[ind], loc="upper left", bbox_to_anchor=(1.1, 0.0, 0.5, 1.0), fontsize=label_font_size[0])
        legend.get_title().set_fontsize(label_font_size[0])


    #plt.setp(autotexts, size=16, weight="bold") 
    return fig
    
