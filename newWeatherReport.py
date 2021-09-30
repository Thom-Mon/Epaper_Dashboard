from urllib.request import urlopen
import re
import requests

def weather_Report_DWD():
    link = 'https://morgenwirdes.de/wetter.php?id=567'
    wholeHtmlAsString = requests.get(link).text

    SearchpatternMax = "\"36\" fill=\"red\">"
    SearchpatternNight = "\"36\" fill=\"blue\">"
    
    SearchpatternRain = "font-size=\"34\">"
    SearchpatternRainZero = "font-size=\"42\">"
    
    SearchpatternEnd = "<"
    
    #For less Code
    Searchpatterns = [SearchpatternMax,SearchpatternNight]
    SearchpatternsRain = [SearchpatternRain,SearchpatternRainZero]
    StorageNames = ['maxTemp', 'nightTemp']

    weatherDataStorage = dict()
 
    index = 0
    
    for searchpattern in Searchpatterns:
        
        IndexOfSearchpattern = 0
        IndexOfNewSearch= 0
        
        data = weatherDataStorage[StorageNames[index]]=[]
        
        while IndexOfSearchpattern != -1:
            IndexOfSearchpattern = wholeHtmlAsString.find(searchpattern, IndexOfNewSearch)
            IndexOfSearchpatternEnd = wholeHtmlAsString.find(SearchpatternEnd, IndexOfSearchpattern+len(searchpattern))
            
            if IndexOfSearchpattern != 0 and IndexOfSearchpattern != -1:
                data.append(wholeHtmlAsString[IndexOfSearchpattern+len(searchpattern):IndexOfSearchpatternEnd])
            IndexOfNewSearch = IndexOfSearchpattern+len(searchpattern)
        
        IndexOfSearchpattern = 0
        IndexOfNewSearch= 0
        index+=1


    #Special Search for Rain Amount, because of the dynamic generated webpage
    indexesOfRainCount = []
    
    for searchpattern in SearchpatternsRain:
        while IndexOfSearchpattern != -1:
            IndexOfSearchpattern = wholeHtmlAsString.find(searchpattern, IndexOfNewSearch)
            
            if IndexOfSearchpattern != 0 and IndexOfSearchpattern != -1:
                indexesOfRainCount.append(int(IndexOfSearchpattern+len(searchpattern)))
            IndexOfNewSearch = IndexOfSearchpattern+len(searchpattern)
        
        IndexOfSearchpattern = 0
        IndexOfNewSearch= 0
    
    indexesOfRainCount.sort()
    
    weatherDataStorage['rainCount'] = []
    
    for index in indexesOfRainCount:
        endText = wholeHtmlAsString.find(SearchpatternEnd, index)
        weatherDataStorage['rainCount'].append(wholeHtmlAsString[index:endText])
    
    return weatherDataStorage

