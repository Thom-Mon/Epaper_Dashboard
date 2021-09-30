#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = '/home/pi/bcm2835-1.60/e-Paper/RaspberryPi_JetsonNano/python/pic'
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd4in2bc
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import datetime

#Imports from Me
from trafficReport import *
from weatherReport import *
from messageReport import *
from newWeatherReport import *

#Position Variables for Drawing#######################################################################
# CHANGE POSITION OF DRAWINGS HERE
#Main
Left_Border = 10
Right_Border = 355

#Weather
DataNumberY = 230
IconPosY = DataNumberY-35

DataCurrTempPosX = 233
DataMaxTempPosX = DataCurrTempPosX+56
DataRainPosX = DataMaxTempPosX+66


#Get Highwayreports for given Entry and Exit...Syntax => GetReportsOnHighway(HighwayName, Entry, Exit)

jam = GetReportsOnHighway("A4", "Kreuz Erfurt", "Magdala")

"""
#Getting Temp and Rain from Website #################################################################

Refactored to the weatherReport-Import

Variables:

MaxTemp => gives maximum Temperature of the Day
CurrentTemp => gives current Temperature reeadings from weatherstation in Jena
numberextract_rain => gives probability of rain in Jena

#Getting Messages from Tageschau Atom######################################################################

Variables:

Message_Board(index on Tagesschau 'https://www.tagesschau.de/xml/atom/'

Example:
Message_Board(0)
#################################################################################################
"""
logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("Dashboard Epaper started")

    epd = epd4in2bc.EPD()
    logging.info("Initializing")
    epd.init()
    epd.Clear()
    time.sleep(1)

        # Setting Time as a Variable
    today = datetime.datetime.now()
    datum = today.strftime("%d.%m.%Y")
    now = today.strftime("%H:%M")

    # FontSizes
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font60 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 60)
    font14 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 13)

    #get newWeatherData
    weatherData = weather_Report_DWD()


    # All Drawing Content
    logging.info("Drawing Dashboard Content")
    HBlackimage = Image.new('1', (epd.width, epd.height), 255)  # 298*126
    HRYimage = Image.new('1', (epd.width, epd.height), 255)  # 298*126  ryimage: red or yellow image
    drawblack = ImageDraw.Draw(HBlackimage)
    drawry = ImageDraw.Draw(HRYimage)

    drawblack.text((Left_Border, 0), u' {}'.format(now), font = font60, fill = 0)
    drawblack.text((Left_Border, 65), 'Datum: {}'.format(datum), font = font24, fill = 0)
    drawblack.text((Left_Border, 110), ' {}'.format(Message_Board(0)), font = font14, fill = 0)
    drawblack.text((Left_Border, 130), ' {}'.format(Message_Board(1)), font = font14, fill = 0)
    drawblack.text((Left_Border, 150), ' {}'.format(Message_Board(2)), font = font14, fill = 0)

    drawblack.text((355, DataNumberY), ' {}'.format(weatherData['rainCount'][0]), font = font18, fill = 0)
    drawblack.text((289, DataNumberY), ' {}°C'.format(weatherData['maxTemp'][0]), font = font18, fill = 0)
    drawblack.text((233, DataNumberY), ' {}°C'.format(CurrentTemp), font = font18, fill = 0)
    
    drawry.text((Left_Border, 170), ' {}'.format(jam), font = font14, fill = 0)
    drawblack.line((Left_Border, 100, 225, 100), fill = 0)
    newimage = Image.open('/home/pi/bcm2835-1.60/e-Paper/RaspberryPi_JetsonNano/python/pic/40x30_rain.bmp')
    HBlackimage.paste(newimage, (349,IconPosY))
    newimage_temp = Image.open('/home/pi/bcm2835-1.60/e-Paper/RaspberryPi_JetsonNano/python/pic/40x30_temp.bmp')
    HBlackimage.paste(newimage_temp, (300,IconPosY))
    newimage_tempcurrent = Image.open('/home/pi/bcm2835-1.60/e-Paper/RaspberryPi_JetsonNano/python/pic/40x30_tempcurrent.bmp')
    HBlackimage.paste(newimage_tempcurrent, (240,IconPosY))
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
    time.sleep(1)

    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd4in2bc.epdconfig.module_exit()
    exit()