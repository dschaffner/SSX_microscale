#paper plotting methods
#Turning code in paper_plot_methods into callable functions
#e.g. import paper_plot_methods as ppm
#     ... ppm.plot1(xData, [yData])

#If you want to include this module in some file f, create a symbolic link
#to this file in the directory containing f: 
# $ ln -l -s <path to this file> paper_plot_methods.py

import matplotlib.pylab as plt
import numpy as np

def __init__(self):
  pass #Allow includes

################################################################
#settings for axes/ticks widths, etc. -> Called for any plotting
################################################################
plt.rc('axes',linewidth=0.75)#axis border widths (I tend to like bolder than the default)
plt.rc('xtick.major',width=0.75)#tick widths (I like them the same width as the border)
plt.rc('ytick.major',width=0.75)
plt.rc('xtick.minor',width=0.75)
plt.rc('ytick.minor',width=0.75)
plt.rc('lines',markersize=4,markeredgewidth=0.0)#size of markers,no outline

#If you want a range of colors, this is a useful function to generate an equally
#spaced range
import matplotlib.cm as cm
num_colors = 9
colors = np.zeros([num_colors,4])#the four is constant
for i in np.arange(num_colors):
    c = cm.spectral(i/float(num_colors),1)
    colors[i,:]=c
#then, call color=colors[x,:] in the plot routine
#AW: this doesn't seem to work.

#These are possible marker styles
points = ['o','v','s','p','*','h','^','D','+','>','H','d','x','<']


###########################################################
#Two subplotting options: call subplot or manually set axes
###########################################################

####Using Subplot####
#default settings for margin (can be tweaked accordingly
left  = 0.2  # the left side of the subplots of the figure
right = 0.95    # the right side of the subplots of the figure
bottom = 0.15   # the bottom of the subplots of the figure
top = 0.95      # the top of the subplots of the figure
wspace = 0.2   # the amount of width reserved for blank space between subplots
hspace = 0.1   # the amount of height reserved for white space between subplots

####################
###Single Subplot###
####################
def plot1(x, yList, xLabel, yLabel, labels, colorList = None,
    pointList = None, lineList = None, savefile='Figure1.png'):
    """
    Make a single plot. 
    Inputs:
    - x: x data series
    - yList: list of y data series
    - xLabel: label for x axis
    - yLabel: label for y axis
    - labels: list of labels for each yList
    Optional Parameters:
    - colorList: list of colors to use. Defaults to blue
    - pointList: list of marker styles to use. Defaults to dots
    - lineList: list of line styles to use. Defaults to solid
    - saveFile: save path
    Returns:
    - Reference to figure; saves plot to savefile
    
    """
    if len(yList[0]) == 1:
      numSeries = 1
      yList = [yList] #Used so that yList is always an array of arrays
    else: numSeries = len(yList[0])
    #If no lineList provided, make lineList all solid
    if lineList == None: lineList = ['-' for i in range(numSeries)]
    if colorList == None: colorList = ['b' for i in range(numSeries)]
    if pointList == None: pointList = ['.' for i in range(numSeries)]
    
    ## Input check: ##
    if len(x) != len(yList[0]): raise Exception('Differing x and y lengths')
    if numSeries != len(labels): raise Exception('Incorrect number of labels')
    if numSeries > len(colorList): raise Exception('Not enough colors')
    if numSeries > len(pointList): raise Exception('Not enough markers')
    if numSeries > len(lineList): raise Exception('Not enough lineStyles')
    
    ## End input check ##
    
    #call figure #3.5x3.5 is a good number for 300dpi
    fig=plt.figure(num=1,figsize=(3.5,3.5),dpi=300,facecolor='w',edgecolor='k')
    #apply settings for margin listed above to the figure
    plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
    #call subplot object
    ax=plt.subplot(1,1,1)#(num rows, num columns, subplot position)
    
    #plot curves
    #normal line plot
    for i, y in enumerate(yList):
      plt.plot(x,y,color=colorList[i],marker=pointList[i], \
        linestyle = lineList[i], linewidth=1.5,label=labels[i])
    #dashed line plot with circle markers
    #plt.plot(x,z,marker='o',color='blue',linestyle='dashed',linewidth=1.5,label='Cos')
    
    #set labels, labels sizes, ticks, ticks sizes
    plt.xlabel(xLabel,fontsize=9)
    plt.ylabel(yLabel,fontsize=9)
    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)
    
    #saving the plot
    #for the paper draft, its best to use png. When we actually submit a paper
    #we'll need to save the plot as a .eps file instead.
    plt.savefig(savefile,dpi=300,facecolor='w',edgecolor='k')
    return fig

#######################################
### Multiple Subplots (same size) #####
#######################################
def plotMultiEven(xList, yList, xLabels, yLabels, labels, colorList = None,
    pointList = points, lineList = None, savefile='Figure1.png'):
    """
    Make multiple subplots.
    Inputs:
    - xList: list of x data series
    - yList: list of y data series. yList[i][j] is the j-th set of data on the i-th plot.
    - xLabels: list of x axis labels
    - yLabels: list of y axis labels
    - labels: list of labels for y data series. 
        labels[i][j] is the label for the series yList[i][j]
    Optional Parameters: (UNLESS multiple series per subplot, in which case
    the ~List parameters must be defined)
    - colorList: list of colors to use. Defaults to 9-color range defined above
    - pointList: list of marker styles to use. Defaults to points above
    - lineList: list of line styles to use. Defaults to solid
    - saveFile: save path
    Returns:
    - Reference to figure; saves plot to savefile
    
    """

    numPlots = len(xList)
    #DS: I've found using a figsize of (3.5,8) for higher numbers of subplots
    #is usually sufficient.
    if numPlots == 2: figsize = (3.5,6)
    else: figsize = (3.5,8)
    
    #If no lineList provided, make lineList all solid
    if lineList == None: lineList = ['-' for i in range(len(yList[0]))]
    if colorList == None: colorList = ['b' for i in range(len(yList[0]))]
    
    '''
    ## Input check: ##
    if len(x) != len(y1) or len(x) != len(y2): raise Exception('Differing x and y lengths')
    if len(yList[0]) != len(labels): raise Exception('Incorrect number of labels')
    if len(yList) > len(colorList): raise Exception('Not enough colors')
    if len(yList) > len(pointList): raise Exception('Not enough markers')
    if len(yList) > len(lineList): raise Exception('Not enough lineStyles')
    
    ## End input check ##
    '''
    
    #call figure #3.5x6 is a good number for 300dpi
    fig=plt.figure(num=2,figsize=figsize,dpi=300,facecolor='w',edgecolor='k')
    #apply settings for margin listed above to the figure
    plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
    
    #call first subplot object
    for i in range(numPlots):
        x = xList[i]
        ax=plt.subplot(numPlots,1,i+1)#(num rows, num columns, subplot position)
        #apply letter label: coordinates in subplot object space (x,y) where (0,0) = bottom left
        #also make sure transform uses correct subplot object)
        plt.text(0.07,0.92,'({})'.format(chr(97+i)),horizontalalignment='center',\
            verticalalignment='center',transform=ax.transAxes)
        #plot curve
        if len(yList[i][0]) == 1: #Only one data series to plot
            print colorList[i], pointList[i], lineList[i], labels[i]
            plt.plot(x,yList[i],color=colorList[i],marker=pointList[i], \
                linestyle = lineList[i], linewidth=1.5, label=labels[i])
        else: #Multiple data series for subplot. 
        #Breaks if the plotting parameters aren't defined
            for j,y in enumerate(yList[i]):
                plt.plot(x ,y,color=colorList[i][j],marker=pointList[i][j], \
                    linestyle = lineList[i][j], linewidth=1.5,label=labels[i][j])
        #set labels, labels sizes, ticks, ticks sizes (Note: only y label, but both x,y ticks)
        plt.ylabel(yLabels[i],fontsize=9)
        plt.xticks(fontsize=9)
        plt.yticks(fontsize=9)
        #plt.xlim(0,20)
        #plt.ylim(-1.5,1.5)
        #suppress xtick values (modify subplot object ax)
        ax.set_xticklabels([])
        
        #Add Zero line (y position, xmin, xmax)
        #plt.hlines(0,0,20,color='red',linestyle='dotted',linewidth=0.5)
        #plt.text(5,0.05,'y=0',fontsize=4,color='red',horizontalalignment='center')
            #(x,y) is in data coordinates when transform is not specified
        #plt.vlines(5,-1.5,1.5,color='gray',linestyle='dashed',linewidth=2.0)
        #plt.vlines(15,-0.75,0.75,color='gray',linestyle='dashed',linewidth=2.0)
    
    #saving the plot
    #for the paper draft, its best to use png. When we actually submit a paper
    #we'll need to save the plot as a .eps file instead.
    plt.savefig(savefile,dpi=300,facecolor='w',edgecolor='k')
    return fig

'''
######################################################
###Two Subplots (Unequal sizes, differe t x-axes)#####
######################################################
#call figure #3.5x6 is a good number for 300dpi
fig=plt.figure(num=3,figsize=(3.5,6),dpi=300,facecolor='w',edgecolor='k')

#First subplot
#settings for margin for first subplot
left  = 0.20  # the left side of the subplots of the figure
right = 0.95    # the right side of the subplots of the figure
bottom = 0.70  # the bottom of the subplots of the figure
top = 0.98      # the top of the subplots of the figure

#make axes object (rather than subplot object)
ax=plt.axes([left,bottom,right-left,top-bottom])
#apply letter label: coordinates in subplot object space (x,y) where (0,0) = bottom left
#also make sure transform uses correct subplot object)
plt.text(0.07,0.92,'(a)',horizontalalignment='center',verticalalignment='center',transform=ax.transAxes)
#plot dotted curve with triangle markers
plt.plot(x,y,marker='^',color='red',linestyle='dotted',linewidth=1.5,label='Sin')
#set labels, labels sizes, ticks, ticks sizes (Note: manually set x ticks)
plt.xlabel('Time [s]',fontsize=9)
plt.ylabel('Power [arb]',fontsize=9)
plt.xticks(np.array([3,5,6,10,15,16,17,18]),fontsize=9)
plt.yticks(fontsize=9)
plt.xlim(0,20)
plt.ylim(-1.5,1.5)

#Second subplot
#settings for margin for first subplot
left  = 0.20  # the left side of the subplots of the figure
right = 0.95    # the right side of the subplots of the figure
bottom = 0.10  # the bottom of the subplots of the figure
top = 0.60      # the top of the subplots of the figure
#make axes object (rather than subplot object)
ax2=plt.axes([left,bottom,right-left,top-bottom])
#apply letter label: coordinates in subplot object space (x,y) where (0,0) = bottom left
#also make sure transform uses correct subplot object)
plt.text(0.07,0.92,'(b)',horizontalalignment='center',verticalalignment='center',transform=ax2.transAxes)
#plot curve with errorbars, dashed with circle markers)
x2 = np.arange(10)/10.
y2 = np.exp(x2)
yerr = 0.1*y2
plt.errorbar(x2,y2,yerr=yerr,marker='o',linestyle='dashed',capsize=2,capthick=0.5,linewidth=1.5,label='Exp')
#set labels, labels sizes, ticks, ticks sizes (Note: manually set x ticks)
plt.xlabel('Distance [m]',fontsize=9)
plt.ylabel('Speed [m/s]',fontsize=9)
plt.xticks(fontsize=9)
plt.yticks(fontsize=9)

#saving the plot
#for the paper draft, its best to use png. When we actually submit a paper
#we'll need to save the plot as a .eps file instead.
savefile='Figure3_2subplots_diffsize.png'
plt.savefig(savefile,dpi=300,facecolor='w',edgecolor='k')
'''