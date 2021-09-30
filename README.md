# Epaper_Dashboard
Epaper Dashboard written in Python for the 4.2" Waveshare (Red/Black) 


Variables:

CurrentTemp => gives current Temperature reeadings from weatherstation in Jena
weatherData ->  contains all information given by "morgenwirdes.de" in an associated array
                the array provides 10 days of information which can be called by the name of 
                information you want and the index refering to the day
    Provided informationtypes:
                maxTemp 
                nightTemp
                rainCount
    Accessing Example:
                weatherData['maxTemp'][1]       -> gives the maximum Temperature for tomorrow
                weatherData['rainCount'][0]     -> gives the liters of rain for today


Variables:

Message_Board(index on Tagesschau 'https://www.tagesschau.de/xml/atom/'

Example:
Message_Board(0) -> gives first message at the refered webpage

