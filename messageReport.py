from urllib.request import urlopen
import re

def Message_Board(Number):
    link = 'https://www.tagesschau.de/xml/atom/'
    f = urlopen(link)
    myfile = f.read()
    NewFinal= str(myfile, 'utf-8')

    Searchpattern = "<title>"
    SearchpatternEnd = "</title>"

    ListofIndexes = []
    IndexOfSearchpattern = 0
    IndexOfNewSearch= 0

#Collect all Indexes of Searchpattern
    while IndexOfSearchpattern != -1:
        IndexOfSearchpattern=NewFinal.find(Searchpattern, IndexOfNewSearch)
        if IndexOfSearchpattern != 0 and IndexOfSearchpattern != -1 and IndexOfNewSearch != 0 :
            ListofIndexes.append(IndexOfSearchpattern+len(Searchpattern))
        IndexOfNewSearch = IndexOfSearchpattern+len(Searchpattern)

#Get Messageboard Content on method call
    IndexOfSearchpatternEnd=NewFinal.find(SearchpatternEnd, ListofIndexes[Number])
    MessageCall=NewFinal[ListofIndexes[Number]:IndexOfSearchpatternEnd]
    #print (MessageCall)

    return MessageCall