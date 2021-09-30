from urllib.request import urlopen
import re

link_currenttemp='http://wetter.mb.eah-jena.de/station/datenbank/php_giese/online.php'
g = urlopen(link_currenttemp)
readtemp = g.read()
read_station=str(readtemp)

searchpattern_temp="Temperatur"
searchpattern_strong="<strong>"
searchpattern_strong_last="\\x"

#Get CurrentTemp
IndexofCurrentTemp= read_station.find(searchpattern_strong,read_station.find(searchpattern_temp)+len(searchpattern_temp))
IndexOfCurrentTempEnd=read_station.find(searchpattern_strong_last, IndexofCurrentTemp)
CurrentTemp= (read_station[IndexofCurrentTemp+len(searchpattern_strong):IndexOfCurrentTempEnd]).strip()