import os
import numpy as np
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

import geopandas as gpd
import matplotlib.pyplot as plt

##-- Getting the Data from webpage --##
def web_scraping (): 

    state, confirmed, cured, dead = [], [], [], []
    
    #-- opening the webpage --#
    driver = webdriver.Chrome(executable_path='/usr/lib/chromedriver')    #--using chrome.
    driver.get("https://www.mygov.in/corona-data/covid19-statewise-status")    #--the webpage.
    
    soup = BeautifulSoup(driver.page_source, 'lxml')    #--extracting the html data.

    #-- getting data --#
    mainTable = soup.find(id='block-system-main')  #--main Table.
    rows = mainTable.findAll(class_='content')     #--rows of the Table.
    
    #-- the summary things --#
    titles = rows[0].findAll(class_='field-items')   #--first two rows contain the subtitles.
    time = titles[0].text
    totalScreened = titles[1].text
    totalActive = titles[2].text
    totalCured = titles[3].text
    totalDead = titles[5].text
    
    #-- extracting the elements --#
    for row in rows[2:]:    #--each row in the Table.
        try:
            fields = row.findAll(class_='field-items')    #--items of each row.
            state.append(fields[0].text)
            confirmed.append(int(fields[1].text))
            cured.append(int(fields[2].text))
            dead.append(int(fields[3].text)) 
        except AttributeError:
            pass
        
    #-- saving to a dataframe --#    
    df = pd.DataFrame({'State':state, 'Confirmed':confirmed, 'Cured':cured, 'Dead':dead}) 
    df = df.sort_values('State', ascending=True)
    df.to_csv('covid19Data_' + time + '.csv')
    #print(df)
    
    #-- saving summary to a txt file --#
    print('\nTime: {0}\nTotalScreened: {1}\nActive Cases: {2}\nDead: {3}'.format(time, totalScreened, totalActive, totalCured, totalDead))
    with open('covid19_summary.txt', 'a') as f:
        f.write('\nTime: {0}\nTotalScreened: {1}\nActive Cases: {2}\nDead: {3}\nCured: {4}\n'.format(time, totalScreened, totalActive, totalDead, totalCured))

    details = [time, totalActive, totalDead, totalCured]
    
    return(df, details)
    

##-- Overlaying on the Map --#
def map_overlay (df, details, toPlot):
   
    time, totalActive, totalDead, totalCured = details[0], details[1], details[2], details[3]

    path = '/media/suyog/DATA/Python/covid19Map'
    
    #dfMap = gpd.read_file(os.path.join(path, 'indiaMapData', 'IND_adm0.shp'))
    #dfMap = gpd.read_file(os.path.join(path, 'GIS_file_of_India_State,_District_and_Tehsil_Boundaries', 'commondata', 'ind_adm_shp', 'IND_adm2.shp'))
    
    dfMap = gpd.read_file(os.path.join(path, 'indiaMapStates', 'Indian_States.shp'))
    dfMap = dfMap.sort_values('st_nm')
   
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
    
    #df = data.drop(['State'], axis=1)
    #df.insert(1, 'State', pd.Series(dfMap.st_nm))
    #print(df)
    
    dfMerged = dfMap.set_index('st_nm').join(df)
    dfMerged = dfMerged.fillna(0)
    
    vmin, vmax = 0, dfMerged.loc[:, toPlot].max()
    
    #-- plotting the map --#
    fig, ax = plt.subplots(figsize=(12, 12))
    dfMerged.plot(column=toPlot, cmap='YlOrBr', ax=ax, linewidth=0.25, edgecolor='black')
    
    sm = plt.cm.ScalarMappable(cmap='YlOrBr', norm=plt.Normalize(vmin=vmin, vmax=vmax))  #--creating the colorbar as legend.
    
    if toPlot=='Confirmed':
        title = toPlot + ' Cases'
        total = totalActive
    elif toPlot=='Dead':
        title = toPlot
        total = totalDead
    elif toPlot=='Cured':
        title = toPlot
        total = totalCured
    
    sm._A = []    #--this empties the array for the data range.
    cbar = fig.colorbar(sm, label='Number of ' + title)    #--adding the colorbar to the figure.
    
    ax.axis('off')
    ax.set_title(title, fontsize=15)
    #ax.text(0.60, 0.85, title, transform=ax.transAxes, ha='left', va='center', fontsize=15)
    ax.text(0.60, 0.8, 'Total = ' + total, transform=ax.transAxes, ha='left', va='center', fontsize=12)
    ax.text(0.05, 0.05, time, transform=ax.transAxes, ha='left', va='center', fontsize=12)
    ax.text(0.05, 0.02, 'https://www.mygov.in/corona-data/covid19-statewise-status', transform=ax.transAxes, ha='left', va='center', fontsize=12)
    
    fig.savefig('covid19Map_' + toPlot + '_' + time + '.png', dpi=300)
    fig.savefig('latestImage_' + toPlot + '.png', dpi=300)
    plt.show()
    plt.close()
   
    return()
    
    
##-- Main Program --##
if __name__=='__main__':

    data, details = web_scraping()
    #map_overlay(data, details, 'Dead')
    
    ans = 'y'
    while ans=='y':
        try:
            toPlot = input('\n\tWhich map do you want (Confirmed/Cured/Dead)?:\t')
            map_overlay(data, details, toPlot)
            ans = input('\n\tDo you want another map(y/n)?:\t')
        except KeyError:
            width = 30
            message = 'Kindly give a valid input'.center(width, ' ')
            print('\n\t\t'+'*'*(width+4))
            print(f'\t\t**{message}**')
            print('\t\t'+'*'*(width+4))
            continue
        
    

#################### End of Program ##############################
##################################################################


