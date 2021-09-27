from urllib.request import urlopen
import re

ListofExists= []

def GetAllExit(HighwayName):
    link = 'http://www.autobahnatlas-online.de/{}.htm'.format(HighwayName)
    f = urlopen(link)
    read_highway_exits = f.read()
    highway_exit_as_string= str(read_highway_exits, 'iso8859_2')


#Problem = The Searchpattern is not absolute on the Website, so it has to be calculated first
    Searchpattern = GetSearchpattern(highway_exit_as_string)
    Searchpattern_end = "<"


    ListofIndexes = []
    IndexOfSearchpattern = 0
    IndexOfNewSearch= 0

#Collect all Exits
    while IndexOfSearchpattern != -1:
        IndexOfSearchpattern=highway_exit_as_string.find(Searchpattern, IndexOfNewSearch)
        IndexOfNewSearch = IndexOfSearchpattern + len(Searchpattern)
        IndexOfEndName = highway_exit_as_string.find(Searchpattern_end ,IndexOfSearchpattern+len(Searchpattern))
        ListofIndexes.append(IndexOfSearchpattern + len(Searchpattern))#werden im fertigen Programm nicht benötigt (DEBUG)

        ExitName=highway_exit_as_string[IndexOfSearchpattern+len(Searchpattern)+1:IndexOfEndName]
        #Delete Empty from List and get only Uppercase-Starting lines

        if ExitName!="" and ExitName[0].isupper()==True:
            ListofExists.append(ExitName)

    return ListofExists


def GetSearchpattern(htmlString):

    highway_exit_as_string=htmlString

    ListOfPossiblePattern=[]
    counter = 0
    IndexOfLoop=0
    for letter in highway_exit_as_string:
        if letter.isupper()==True and highway_exit_as_string[IndexOfLoop]!= highway_exit_as_string[IndexOfLoop-1]:
            counter+=1
            #highway_exit_as_string
        else:
            counter= 0
        if counter == 5:
            IndexOfPattern=IndexOfLoop-20
            SearchPattern = highway_exit_as_string[IndexOfPattern:IndexOfPattern+21]
            IndexOfCapitalletter=0
            for UpperLetters in SearchPattern:
                if UpperLetters.isupper()==True:
                    IndexOfCapitalletter+=1
            if IndexOfCapitalletter >= 12:
                counter=0
                continue
            res = ''.join(filter(lambda i: i.isdigit(), SearchPattern))
            ListOfPossiblePattern.append(res)
            #break
        IndexOfLoop+=1

    #Get Numbers with the highest count in the list
    #Get from all Possible Detection the highest connecting "xl" Nr (next to the found ExitName) ->hat noch Verbesserungsbedarf (Digit Detection!!!!)
    ListOfUnique=[]
    for number in ListOfPossiblePattern:
        if number in ListOfUnique:
            continue
        else:
            ListOfUnique.append(number)
    StartCount=0
    for number in ListOfUnique:
        if StartCount<ListOfPossiblePattern.count(number):
            StartCount = ListOfPossiblePattern.count(number)
            Final=number
    #print("Suchparameter = ", Final)
    return "xl"+Final



def GetHighwaypart(ListOfAllExits, Entrance, Exit): #(List, Entrance, Exit):
    AuffahrtIndex = ListOfAllExits.index(Entrance)
    AbfahrtIndex = ListOfAllExits.index(Exit)
    #print("Ihr gewählter Autobahnbereich: ")

    ListOfAreaExits = []        #Takes all Exits along the Road the User has set
    while AuffahrtIndex<=AbfahrtIndex:
        ListOfAreaExits.append(ListOfAllExits[AuffahrtIndex])
        AuffahrtIndex+=1

    #print("Auffahrt: ", AuffahrtIndex, "Abfahrt: ", AbfahrtIndex)
    #print(*ListOfAreaExits, sep='\n')
    return ListOfAreaExits
    #print("Letzte Abfahrt: ", len(ListOfExits))





def MakeExitNamesReadable(ExitNames):
    ListofExits = []

    fileRead = ExitNames
    minus = "-"

    # fileRead.close()

    for line in fileRead:

        FinalExitName = []
        line_stripped_replaced = ""

        line_stripped = line.strip()

        if line_stripped.find(minus) != -1 and line_stripped.find(" ") != -1:
            # print("minus drin")
            line_stripped_deleted_spaces = line_stripped  # .replace(" ", "")
            counter = 0
            for letter in line_stripped_deleted_spaces:
                if counter != 0 and line_stripped_deleted_spaces[counter - 1].isalpha():
                    if letter.isalpha():
                        ChangedLetter = letter.lower()
                    elif letter == " " and line_stripped_deleted_spaces[counter + 1] == minus:
                        ChangedLetter = ""
                    else:
                        ChangedLetter = letter
                    FinalExitName.append(ChangedLetter)
                elif letter == " " and line_stripped_deleted_spaces[counter - 1] == minus:
                    ChangedLetter = ""
                    FinalExitName.append(ChangedLetter)
                else:
                    ChangedLetter = letter.upper()
                    FinalExitName.append(ChangedLetter)
                counter += 1
            for letters in FinalExitName:
                line_stripped_replaced += letters
        elif line_stripped.find(minus) == -1 and line_stripped.find(" ") == -1:
            line_stripped_replaced = line_stripped.capitalize()
        else:
            counter = 0
            line_stripped_capitalized_only = line_stripped.capitalize()
            for letter in line_stripped_capitalized_only:
                if counter != 0 and line_stripped_capitalized_only[counter - 1] == " ":
                    ChangedLetter = letter.upper()
                    FinalExitName.append(ChangedLetter)
                else:
                    FinalExitName.append(letter)
                counter += 1
            for letters in FinalExitName:
                line_stripped_replaced += letters

        ListofExits.append(line_stripped_replaced)

    #print("Anzahl Exits: " + str(len(ListofExits)))

    #for element in ListofExits:
     #   print(element)
    return ListofExits

def GetReportsByExits(HighwayName, ListOfExitsAlong):
    # Staumeldungen Abrufen (LIVE, nicht zu oft machen, wird sonst als DDOS-Angriff gewertet.
    link = 'https://stau.info/autobahn/{}'.format(HighwayName)
    f = urlopen(link)
    read_reports = f.read()
    highway_reports_as_string = str(read_reports)

    #Debug Staumeldungen (Speicher auf Platte für spätere Zugriffe)
    #f = open("c:\\Users\Flodi\Desktop\StaumeldungOffline.txt", "w")
    #f.write(highway_reports_as_string)
    #f.close()

    #fileRead=open("c:\\Users\Flodi\Desktop\StaumeldungOffline.txt", "r")
    #highway_reports_as_string=fileRead.read()
    #fileRead.close()
    ListExampleExits=ListOfExitsAlong
    #print(highway_reports_as_string)

    #1. Tiefe: Wird Autobahnabfahrt überhaupt genannt? Wenn da keine Treffer, dann ist weitere Suche unnötig.
    IndexOfReport=0
    for Exit in ListExampleExits:
        if highway_reports_as_string.find(Exit)!=-1:
            IndexOfReport = highway_reports_as_string.find(Exit)
            if IndexOfReport!=0:
                if highway_reports_as_string.find("Diese Meldung ist aufgehoben", IndexOfReport, IndexOfReport+1000)!=-1 or highway_reports_as_string.find("keine Verkehrsbehinderung", IndexOfReport, IndexOfReport+1000)!=-1:

                    IndexOfReport=0
    if IndexOfReport!=0:
        #print("Verkehrsmeldungen liegen für Auswahl vor!")
        # 2. Tiefe: Verbindungen der Abfahrten zueinander herstellen. Betrifft es vielleicht Gegenrichtung? (Nur wenn #1 etwas gefunden hat)
        for Enter in ListExampleExits:
            for Exit in ListExampleExits:
                Concat = Enter + " und " + Exit
                FoundOnConcat = highway_reports_as_string.find(Concat)
                if FoundOnConcat != -1:
                    print(Concat, " : ", FoundOnConcat)
        IndexOfReport=1
    else:
        IndexOfReport=0

    return IndexOfReport


def GetReportsOnHighway(Highway, Entrance, Exit): #
    #print("Gesamtfunktionstest:")
    Allexits=GetAllExit(Highway) #Variable überflüssig. Zur Änderung offen lassen!!!!!
    #print (Allexits)
    Allexits_no_upper = MakeExitNamesReadable(Allexits)
    #print (Allexits_no_upper)
    Allexits_no_upper_only_part = GetHighwaypart(Allexits_no_upper, Entrance, Exit)
    #print( Allexits_no_upper_only_part)
    finalReport = GetReportsByExits(Highway, Allexits_no_upper_only_part)
    return finalReport