from urllib.request import urlopen
import re

link = 'https://www.wetter.de/deutschland/wetter-jena-18234574.html?q=jena'
f = urlopen(link)
read= f.read()
read_wetter_de=str(read, 'utf-8')

link_currenttemp='http://wetter.mb.eah-jena.de/station/datenbank/php_giese/online.php'
g = urlopen(link_currenttemp)
readtemp = g.read()
read_station=str(readtemp)

searchpattern_rain="wahrscheinlichkeit beträgt"

searchpattern_maxtemp="heute maximal"
searchpattern_the_n="\\n"
searchpattern_Grad="Grad"

searchpattern_temp="Temperatur"
searchpattern_strong="<strong>"
searchpattern_strong_last="\\x"

#Get RainPossibity
IndexOfRain=read_wetter_de.find(searchpattern_rain)
Rain= read_wetter_de[IndexOfRain+len(searchpattern_rain):IndexOfRain+50]
numberextract_rain = ''.join(filter(lambda i: i.isdigit(), Rain))
#Get MaxTemp
IndexOfMaxTemp=read_wetter_de.find(searchpattern_the_n,read_wetter_de.find(searchpattern_maxtemp)+len(searchpattern_maxtemp))
IndexOfMaxTempEnd=read_wetter_de.find(searchpattern_Grad, IndexOfMaxTemp)
MaxTemp= (read_wetter_de[IndexOfMaxTemp+len(searchpattern_the_n):IndexOfMaxTempEnd]).strip()
#Get CurrentTemp
IndexofCurrentTemp= read_station.find(searchpattern_strong,read_station.find(searchpattern_temp)+len(searchpattern_temp))
IndexOfCurrentTempEnd=read_station.find(searchpattern_strong_last, IndexofCurrentTemp)
CurrentTemp= (read_station[IndexofCurrentTemp+len(searchpattern_strong):IndexOfCurrentTempEnd]).strip()