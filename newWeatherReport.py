from urllib.request import urlopen
import re
import requests #necessary wg. https (vielleicht 2 Versionen machen je nach python-Version)

def weather_Report_DWD():
    link = 'https://morgenwirdes.de/wetter.php?id=567'
    wholeHtmlAsString = requests.get(link).text
    #print(r)
    #f = urlopen(link)
    #wholeHtml = f.read()
    #wholeHtmlAsString = str(wholeHtml, 'utf-8')

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
        
        if StorageNames[index] == 'rainCount':
            startLimit = 0
        else:
            startLimit = 0
        
        while IndexOfSearchpattern != -1:
            IndexOfSearchpattern = wholeHtmlAsString.find(searchpattern, IndexOfNewSearch)
            IndexOfSearchpatternEnd = wholeHtmlAsString.find(SearchpatternEnd, IndexOfSearchpattern+len(searchpattern))
            
            if IndexOfSearchpattern != 0 and IndexOfSearchpattern != -1:
                data.append(wholeHtmlAsString[IndexOfSearchpattern+len(searchpattern)+startLimit:IndexOfSearchpatternEnd])
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



#allMaxTemperatures = weather_Report_DWD()   #Namen noch ändern TODO:


#counter = 0
#for index in allMaxTemperatures['maxTemp']:
#    print (index + "___" + allMaxTemperatures['nightTemp'][counter] + "___" + allMaxTemperatures['rainCount'][counter]) 
#    
#    counter += 1
    
#for index in allMaxTemperatures['rainCount']:
 #   print (index)
    
#for index in allMaxTemperatures['rainCount']:
 #   print (index) 

