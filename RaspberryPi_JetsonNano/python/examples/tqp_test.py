#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13bc
import time
import pytz
from datetime import datetime
from PIL import Image,ImageDraw,ImageFont
import traceback
import subprocess

logging.basicConfig(level=logging.DEBUG)

try:
    epd = epd2in13bc.EPD()

    #logging.info("Init and Clear Screen")
    epd.init()
    #epd.Clear()
    #time.sleep(1)
    
    # Set Fonts
    font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font16 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16)
    font14 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14)
    font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
    font10 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 10)
    
    # Drawing on the Horizontal image
    logging.info("Drawing on the Horizontal image...") 
    
    HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
    HRYimage =    Image.new('1', (epd.height, epd.width), 255)  # 298*126  ryimage: red or yellow image  
    drawblack =   ImageDraw.Draw(HBlackimage)
    drawred =     ImageDraw.Draw(HRYimage)

    logging.info("H: %s, W: %s", epd.height, epd.width)

    # Title
    #drawblack.line((0, 17, 212, 17), fill = 0)
    drawblack.rectangle((0, 0, 212, 17), fill = 0)
    drawblack.text((4, 0), 'GPS Tracker ', font = font14, fill = 1)

    # IP Address
    # /sbin/ip -o -4 addr list wlan0 | awk '{print $4}' | cut -d/ -f1
    ipAddress = subprocess.check_output('ifconfig wlan0 | grep \'inet \' | awk \'{print $2}\'', shell=True, text=True)
    drawblack.text((4, 19), 'IP Address: ', font = font12, fill = 0)
    drawblack.text((100, 19), ipAddress, font = font12, fill = 0)
   
    # PiSugar2 Battery Level
    # echo "get battery" | nc -q 0 127.0.0.1 8423
    batteryPercentage = subprocess.check_output('echo \"get battery\" | nc -q 0 127.0.0.1 8423', shell=True, text=True)
    batteryPercentage = batteryPercentage.replace("battery: ", "")
    batteryPercentage = "{:.1f}".format(float(batteryPercentage)) + "%"
    isBatteryCharging = subprocess.check_output('echo \"get battery_charging\" | nc -q 0 127.0.0.1 8423', shell=True, text=True)
    drawblack.text((4, 33), 'PiSugar2 Battery: ', font = font12, fill = 0)
    drawblack.text((100, 33), batteryPercentage, font = font12, fill = 0)

    # Last Location
    lastLocation = "30°14'N, 85°34'W" + " "
    drawblack.text((4, 47), 'Last Location: ', font = font12, fill = 0)
    drawblack.text((100, 47), lastLocation, font = font12, fill = 0)
   
    # Distance to Destination
    distanceToDestination = "23.5 miles" + " "
    drawblack.text((4, 61), 'Dist. to Dest.: ', font = font12, fill = 0)
    drawblack.text((100, 61), distanceToDestination, font = font12, fill = 0)
    
    # Distance from Origin
    distanceFromOrigin = "15.2 miles" + " "
    drawblack.text((4, 75), 'Dist. from Origin: ', font = font12, fill = 0)
    drawblack.text((100, 75), distanceFromOrigin, font = font12, fill = 0)

    # Updated Timestamp
    drawblack.rectangle((0, 90, 212, 104), fill = 0)
    tz = pytz.timezone('America/Chicago') # America_New_York
    dateTimeObj = datetime.now(tz)
    timestampStr = dateTimeObj.strftime("%d-%b-%Y %H:%M:%S")
    drawblack.text((4, 90), 'Last Updated: ' + timestampStr, font = font10, fill = 1)

    #drawblack.line((20, 50, 70, 100), fill = 0)
    #drawblack.line((70, 50, 20, 100), fill = 0)
    #drawblack.rectangle((20, 50, 70, 100), outline = 0)    
    
    #drawred.rectangle((0, 0, 212, 104), fill = 0)
    #drawred.line((165, 50, 165, 100), fill = 0)
    #drawred.line((140, 75, 190, 75), fill = 0)
    #drawred.arc((140, 50, 190, 100), 0, 360, fill = 0)
    #drawred.rectangle((80, 50, 130, 100), fill = 0)
    #drawred.chord((85, 55, 125, 95), 0, 360, fill =1)
    
    #drawblack.text((5, 5), 'Panama City, Florida ', font = font20, fill = 0, align='left')
    
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13bc.epdconfig.module_exit()
    exit()
