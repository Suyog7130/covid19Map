# COVID-19 India Map              

### This code is to generate a map of COVID-19 case distribution in terms of number of Confirmed, Cured and Dead. 

The data used is available at the following webpage: 
https://www.mygov.in/corona-data/covid19-statewise-status 

The new libraries used are:
- __Selenium__, a web testing library used to automate browser activity.
- __BeautifulSoup__, Python package for parsing HTML and XML docs. It creates parse trees that is helpful to 
extract the data easily.
- __Geopandas__, an open source geographic data plotting library. It is primarily used to make choropleth maps.

https://www.naturalearthdata.com/ is a public domain library of map data for the whole world. 
For India, the data can be downloaded from https://www.diva-gis.org/gdata.
There are numerous other places to download the data.
The best one is: https://www.arcgis.com/home/item.html?id=cba8bddfa0ab43ddb35a7313376f9438.

The following the steps were taken to obtain the map:

   1. Finding an accurate government source for the data.
   2. Writing the code to do the web scraping. This is done using selenium and BeautifulSoup. 
   3. Making a pandas table and checking if the data scraped is indeed
      correct. 
   4. Getting a hang of how the geographical data is saved in gis file formats like the shapefiles (.shp).
   5. Generating a map of India with state boundaries. 
   6. Writing the code ot overlay the data scraped from the website onto generated map. This is done used geopandas.
   7. Finally, asking the user for the type of map. 
      Checking how the updation of the website affects this.
      
For the map used in the code, the gis file can obtained from this Google Drive [link](https://drive.google.com/open?id=1Hv9pES2FWrj6xOcQazKb5Mgt2ZqveMPS). 

The extracted data from the webpage is saved into a csv file: [covid19Data](https://github.com/Suyog7130/covid19Map/blob/master/covid19Data_07%20April%202020%2C%2009:00%20GMT%2B5:30.csv). The output map is saved as a png image. [covid19_summary.txt](https://github.com/Suyog7130/covid19Map/blob/master/covid19_summary.txt) contains the overall summary of the number of cases for all the times that the code has been run.

Whenever the code is run, the latest data is extracted from the webpage. This webpage is static, so __*lxml*__ extracts a html page when the code is run and not a javascript file. I use chrome for opening the webpage before the data can be extracted. A separate webdriver is required for this which can be downloaded from (https://chromedriver.chromium.org/).

<!--- Another program can be written which will automate the running of this code, so that the variation of the geographic distribution can be monitored continously. Other types of overlayes can also done on the geographic maps, for instance, bubble maps. They can be made interactive using packages like plotly. The awesome interactive map on the [WHO dashboard](https://who.sprinklr.com/) is one such tool. <!--- which uses their own proprietry programs to generate the plots. -->

[comment]: # (This is a comment)

<!--- I didn't do this because the state or territorial map of India is not available within the plotly library. Nor any other open source geographical data is available, which can be used to get the interactive plot, apart from GeoJSON that is and it's gonna take me a while learn using that. --->
      
The latest maps generated in the last run of the is given below. 

![Dead](https://github.com/Suyog7130/covid19Map_localSync/blob/master/latestImage_Dead.png)

<!--- ![Confirmed Cases](https://github.com/Suyog7130/covid19Map/blob/master/gimp_Confirmed.gif) --->
