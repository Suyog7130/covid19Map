
########################################################
###                  COVID-19 India Map              ###
########################################################

"""
5th and 6th April 2020:
This is to do the web scraping and make the gis map of India
with the COVID-19 casualities bubbles overlayed. 

The Webpage used is available at: 
https://www.mygov.in/corona-data/covid19-statewise-status 

Gonna tackle this in steps. The following the things:

   1. Finding out how data is taken from some website. 
   2. Writing the code to do the web scraping; getting the correct 
      data.
   3. Making a pandas table and checking if the data scraped is indeed
      correct. 
   4. Getting a hang of follium and how the GIS system works.
   5. Making a map of India with the state names and all that. 
   6. Writing the code for the using the follium to overlay the info
      obtained onto the map of India.
   7. Seemlessly merging the two. Saving the data and the plot. 
      Checking how the updation of the website affects this.
      
The new libraries used are Selenium, a web testing library used to automate 
browser activity and BeautifulSoup, Python package for parsing HTML and XML 
docs. It creates parse trees that is helpful to extract the data easily.

NOTE: When copying the files, if some permission is denied then 'nautilus' 
can be used to open the folders in the admin mode. 
'sudo -H nautilus'

The comments within the functions are just the things I wasn't able to get right.
This webpage is static, so that a html doc is returned by lxml and not a javascript file.

https://www.naturalearthdata.com/ is a public domain library of map data for the whole world. 
For India, the data can be downloaded from 'https://www.diva-gis.org/gdata'
There are numerous other places to download the data.
The best one is: 'https://www.arcgis.com/home/item.html?id=cba8bddfa0ab43ddb35a7313376f9438'.

This data is saved in the form of a shapefile, format '.shp'.
This can be used alongwith geopandas, basemap and geoplot to make the map. Goepandas primarily 
eases making the choropleth maps.
To have it interactive or have a choropleth map, other libraries like bokeh and json
can be used in the code. Right now, I ain't gonna do that.

7th April 2020:
Plotly can be used to make the interactive maps. 
The 'go' in the plotly package is a library of graphical objects.
"""

import os
import numpy as np
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

import geopandas as gpd
import matplotlib.pyplot as plt

#import plotly.plotly as py
#import plotly.graph_objs as go 
#from plotly.offline import download_plotlyjs, plot, iplot  

##-- Getting the Data from webpage --##
def web_scraping (): 

    """
    I could have used this, driver = webdriver.Chrome(executable_path='chromedriver.exe') at the start.
    driver = webdriver.Chrome(executable_path='/usr/lib/chromedriver') #("/path/to/chromedriver")    

    driver.get("https://www.mygov.in/corona-data/covid19-statewise-status")
    #content = driver.page_source
    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    #field field-name-field-covid-statewise-data field-type-field-collection field-lable-above.
    #'div', href=True, attrs={'class':'content'}
    """
    """ 
    Different classes present on the webpage are, 'field-items', 'field-item even', 'field-item odd',
    'content' etc. 
    The main table is inside id, 'block-system-main' under class, 'content clearfix'.
    I can look up for the content class for each row of the table.
    Each 'content' corresponds to a row of the table. Each row has four 'field-items' classes.
    
    By chance, the first few subtitle lines are all contained in the first row that is taken out. 
    The contents of the first row are then copied to the second row as well, prob. because of another
    'content'. The actual table with the count of cases comes after that, i.e. from 3rd row.
    """
    """
    result = soup.find(id='block-system-main')    #--the main table.
    x = result.findAll(class_='content')   #--contains the rows of the table.
    
    #print(len(x), x[0])
    
    for i in x:   #--for each row.
        fields = i.findAll(class_='field-items')   #--items of each row. Number of items varies.
        print(fields[4].text, fields[6].text)
        #print('{0} & {1} & {2} & {3}'.format(fields[0].text, fields[1].text, fields[2].text, fields[3].text))
    #print(len(fields))
    """
    
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
        f.write('\nTime: {0}\nTotalScreened: {1}\nActive Cases: {2}\nDead: {3}\n'.format(time, totalScreened, totalActive, totalCured, totalDead))
    
    return(df, time)
    

##-- Overlaying on the Map --#
def map_overlay (df, time):
    """
    The shapefiles for the maps of India are saved inside the folders present in the 
    Python folder. 'os.path' 
    The two data files are first joined together and then the the geopandas library is 
    used to map out the data. 
    To have a consistent seamless naming, the dataframes are sorted in the alphabetical 
    order first and the state names from one are then copied to the other. This copying 
    is done using 'df.drop' and 'df.insert(axis, column_name, df_Series)'
    Alas! These didn't work properly. 
    
    To fill null values with 0, df.filna(0)
    """

    path = '/media/suyog/DATA/Python/covid19Map'
    
    #dfMap = gpd.read_file(os.path.join(path, 'indiaMapData', 'IND_adm0.shp'))
    #dfMap = gpd.read_file(os.path.join(path, 'GIS_file_of_India_State,_District_and_Tehsil_Boundaries', 'commondata', 'ind_adm_shp', 'IND_adm2.shp'))
    
    dfMap = gpd.read_file(os.path.join(path, 'indiaMapStates', 'Indian_States.shp'))
    dfMap = dfMap.sort_values('st_nm')
    
    #-- renaming the state names --#
    for i in range(len(df)):
        if df.loc[i, 'State']=='AndamanNicobar':
            df.loc[i, 'State'] = 'Andaman & Nicobar Island'
        elif df.loc[i, 'State']=='AndhraPradesh':
            df.loc[i, 'State'] = 'Andhra Pradesh'
        elif df.loc[i, 'State']=='HimachalPradesh':
            df.loc[i, 'State'] = 'Himachal Pradesh'
        elif df.loc[i, 'State']=='J & K':    #--adding the ladakh count.
            df.loc[i, 'Confirmed'] = float(df[df.State=='J & K'].Confirmed) + float(df[df.State=='Ladakh'].Confirmed)
            df.loc[i, 'Cured'] = float(df[df.State=='J & K'].Cured) + float(df[df.State=='Ladakh'].Cured)
            df.loc[i, 'Dead'] = float(df[df.State=='J & K'].Dead) + float(df[df.State=='Ladakh'].Dead)
            df.loc[i, 'State'] = 'Jammu & Kashmir'
        elif df.loc[i, 'State']=='MP':
            df.loc[i, 'State'] = 'Madhya Pradesh'
        elif df.loc[i, 'State']=='Delhi':
            df.loc[i, 'State'] = 'NCT of Delhi'
        elif df.loc[i, 'State']=='Arunachal Pradesh':
            df.loc[i, 'State'] = 'Arunanchal Pradesh'
        elif df.loc[i, 'State']=='UttarPradesh':
            df.loc[i, 'State'] = 'Uttar Pradesh'
        elif df.loc[i, 'State']=='TamilNadu':
            df.loc[i, 'State'] = 'Tamil Nadu'
        elif df.loc[i, 'State']=='Telengana':
            df.loc[i, 'State'] = 'Telangana'
    
    #df = data.drop(['State'], axis=1)
    #df.insert(1, 'State', pd.Series(dfMap.st_nm))
    #print(df)
    
    dfMerged = dfMap.set_index('st_nm').join(df.set_index('State'))
    dfMerged = dfMerged.fillna(0)
    #print(dfMerged.head())
    
    toPlot = input('\n\tWhich map do you want (Confirmed/Cured/Dead)?:\t')
    vmin, vmax = 0, dfMerged.loc[:, toPlot].max()
    
    #-- plotting the map --#
    fig, ax = plt.subplots(figsize=(12, 12))
    dfMerged.plot(column=toPlot, cmap='YlOrBr', ax=ax, linewidth=0.25, edgecolor='black')
    
    sm = plt.cm.ScalarMappable(cmap='YlOrBr', norm=plt.Normalize(vmin=vmin, vmax=vmax))  #--creating the colorbar as legend.
    
    if toPlot=='Confirmed':
        title = toPlot + ' Cases'
    else:
        title = toPlot
    
    sm._A = []    #--this empties the array for the data range.
    cbar = fig.colorbar(sm, label='Number of ' + title)    #--adding the colorbar to the figure.
    
    ax.axis('off')
    ax.set_title(title, fontsize=15)
    ax.text(0.05, 0.05, time, transform=ax.transAxes, ha='left', va='center', fontsize=12)
    ax.text(0.05, 0.02, 'https://www.mygov.in/corona-data/covid19-statewise-status', transform=ax.transAxes, ha='left', va='center', fontsize=12)
    
    fig.savefig('covid19Map_' + toPlot + '_' + time + '.png', dpi=300)
    plt.show()
    plt.close()
    
    """
    Nope this cannot be done. The scope available is either the world, us or continents.
    #-- plotting an interactive map --#
    dataToPlot = dict(type='choropleth',
                      locations = dfMerged.index,
                      locationmode = 'USA-states',
                      colorscale = 'YlOrBr',
                      text = toPlot,
                      z = dfMerged[toPlot],
                      colorbar = {'title':'Number of ' + title})
    layout = dict(title = title, geo = {'scope':'asia'})
    choromap = go.Figure(data = [dataToPlot], layout = layout)  #--makes the plot.
    iplot(choromap)    #--generates the interactive plot.
    """
    
    return()
    
    
##-- Main Program --##
if __name__=='__main__':

    data, time = web_scraping()
    ans = 'y'
    while ans=='y':
        map_overlay(data, time)
        ans = input('\n\tDo you want another map(y/n)?:\t')
    
    
    

#################### End of Program ##############################
##################################################################


