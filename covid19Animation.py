import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML


##-- the function to that will be called multiple times for animation --##
def animateMap (fig, time, toPlot, maxCount):
    
    #-- getting the data file of the said date and time --#
    file_name = 'covid19Data_' + time + '.csv'
    df = pd.read_csv(file_name)
    
    total = df.loc[:, toPlot].sum() 
    maxCount = float(maxCount)   
    
    #-- getting the map data --#
    path = '/media/suyog/DATA/Python/covid19Map'
    dfMap = gpd.read_file(os.path.join(path, 'indiaMapStates', 'Indian_States.shp'))
    
    dfMap = dfMap.sort_values('st_nm')   #--sorting wrt state names.

    #-- adding ladakh count to J&K --#
    for i in range(len(df)):
        if df.loc[i, 'State']=='J & K':   #--this is done only once, the next time this is not true.
            df.loc[i, 'Confirmed'] = float(df[df.State=='J & K'].Confirmed) + float(df[df.State=='Ladakh'].Confirmed)
            df.loc[i, 'Cured'] = float(df[df.State=='J & K'].Cured) + float(df[df.State=='Ladakh'].Cured)
            df.loc[i, 'Dead'] = float(df[df.State=='J & K'].Dead) + float(df[df.State=='Ladakh'].Dead)
            df.loc[i, 'State'] = 'Jammu & Kashmir'      
    
    #-- renaming the states --# 
    df = df.set_index('State')
    df.rename(index={'AndamanNicobar':'Andaman & Nicobar Island', 'AndhraPradesh':'Andhra Pradesh',
                     'HimachalPradesh':'Himachal Pradesh', 'MP':'Madhya Pradesh',
                     'Delhi':'NCT of Delhi', 'Arunachal Pradesh':'Arunanchal Pradesh',
                     'UttarPradesh':'Uttar Pradesh', 'TamilNadu':'Tamil Nadu', 'Telengana':'Telangana'
                     }, inplace='True')
    
    #-- merging the data with the geo dataframe --#
    dfMerged = dfMap.set_index('st_nm').join(df)
    dfMerged = dfMerged.fillna(0)

    if toPlot=='Confirmed':
        title = toPlot + ' Cases'
    elif toPlot=='Dead':
        title = toPlot
    elif toPlot=='Cured':
        title = toPlot
    
    #-- plotting the map --#
    vmin, vmax = 0, maxCount
    cmap = 'YlOrBr' #'tab20b' 
    dfMerged.plot(column=toPlot, cmap=cmap, ax=ax, linewidth=0.25, edgecolor='black', vmin=vmin, vmax=vmax)
    
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))  #--creating the colorbar as legend.
    
    sm._A = []    #--this empties the array for the data range.
    cbar = fig.colorbar(sm, label='Number of ' + title, ticks=np.arange(0, maxCount, maxCount/10))    #--adding the colorbar to the figure.
 
    ax.axis('off')
    #ax.set_title(title, fontsize=15)
    ax.text(0.60, 0.85, title, transform=ax.transAxes, ha='left', va='center', fontsize=15)
    ax.text(0.60, 0.8, 'Total = ' + str(total), transform=ax.transAxes, ha='left', va='center', fontsize=12)
    ax.text(0.05, 0.05, time, transform=ax.transAxes, ha='left', va='center', fontsize=12)
    ax.text(0.05, 0.02, 'https://www.mygov.in/corona-data/covid19-statewise-status', transform=ax.transAxes, ha='left', va='center', fontsize=12)
    
    path = os.path.join(toPlot, time)
    plt.savefig(path + '_' + toPlot + '.png', dpi=300)
    #plt.show()
    plt.close()

    #print(dfMerged.Confirmed)
    return ()


##-- main Program --##
if __name__=='__main__':
    
    df0 = pd.read_csv('dataFile_names.txt', sep='\n', header=None)
    df0.columns = ['file_name']
    fnames = df0.file_name.tolist()
    #print(fnames, len(fnames))

    periods = []
    for f in fnames:
        periods.append(f[12:len(f)-4])   #--extracting the date and time of getting the data.
    #print(periods)
    
    try:
        toPlot = input('\n\tWhich map do you want (Confirmed/Cured/Dead)?:\t')
        maxCount = input('\tGive the value of max {} cases (Confirmed=7500, Dead=300):\t'.format(toPlot))
        for p in periods:
            fig, ax = plt.subplots(figsize=(12, 12))
            animateMap(fig, p, toPlot, maxCount)

    except KeyError:
        width = 30
        message = 'Kindly give a valid input'.center(width, ' ')
        print('\n\t\t'+'*'*(width+4))
        print(f'\t\t**{message}**')
        print('\t\t'+'*'*(width+4))

#################### End of Program ##############################
##################################################################


