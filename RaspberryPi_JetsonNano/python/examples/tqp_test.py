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

logging.basicConfig(level=logging.DEBUG)

try:
    epd = epd2in13bc.EPD()

    #logging.info("Init and Clear Screen")
    epd.init()
    epd.Clear()
    #time.sleep(1)
    
    # Set Fonts
    font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
    font10 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 10)
    
    # Drawing on the Horizontal image
    logging.info("Drawing on the Horizontal image...") 
    
    HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
    HRYimage =    Image.new('1', (epd.height, epd.width), 255)  # 298*126  ryimage: red or yellow image  
    drawblack =   ImageDraw.Draw(HBlackimage)
    drawred =     ImageDraw.Draw(HRYimage)

    logging.info("H: %s, W: %s", epd.height, epd.width)

    drawblack.text((4, 2), 'Panama City, Florida ', font = font20, fill = 0)
    drawblack.line((0, 28, 212, 28), fill = 0)

    drawblack.rectangle((0, 90, 212, 104), fill = 0)

    # America/New_York
    # America/Chicago 
    #   
 
    tz = pytz.timezone('America/Chicago')
    dateTimeObj = datetime.now(tz)
    timestampStr = dateTimeObj.strftime("%d-%b-%Y %H:%M:%S")
    drawblack.text((4, 90), 'Updated: ' + timestampStr, font = font10, fill = 1)

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
