import pyautogui as pg
import sys
import re
import os
import glob
from time import time
from time import sleep
from pyzbar import pyzbar
from imutils.video import FileVideoStream
import imutils
import argparse
import cv2

def getLink(): #get the line of selected google meet link
    try:
        linkSelect = int(input('Please enter the digit of your selected google meet link; eg: 1,2,3,...\n'))
    except ValueError:
        print('Error, please enter only digits')
        getLink()
    return linkSelect

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
meetlink = os.path.join(THIS_FOLDER, 'meetlink.txt')

hours = time() // 3600 #start timer

i = 0
with open(meetlink, 'r') as fp:
    for lines in (fp.read().split('\n'))[2:]: #output selection of meet link
        i += 1
        print(str(i) + ': ' + lines)

with open(meetlink, 'r') as fp:
    mo = re.findall('https.*', fp.read())
link = mo[getLink()-1] #store google meet link to 'link' variable

pg.hotkey('winleft') #press windows key on keyboard
sleep(1)
pg.typewrite('chrome\n',0.1) #type in chrome in search bar and enter
sleep(5)
pg.typewrite(link + '\n') #enter link from meetlink.txt
pg.hotkey('winkey','up') #fullscreen google chrome
sleep(5)
pg.hotkey('ctrl','d') #mute mic
sleep(1)
pg.hotkey('ctrl','e') #hide cam

pg.click(1271,596) #join classroom
sleep(1)
pg.click(1680,125) #show chat

#open obs
pg.hotkey('winleft') #press windows key on keyboard
sleep(1)
pg.typewrite('obs\n',0.1)
sleep(4)

#start recording , requires start recording and stop recording hotkey
pg.hotkey('f1')
sleep(1)
pg.hotkey('alt','\t') #alt tab into chrome

#QR scanner
while True:
        pg.screenshot('ss.png') #take a screenshot
        image = cv2.imread('ss.png') # load the screenshot

        # find the barcodes in the image and decode each of the barcodes
        barcodes = pyzbar.decode(image)

        # loop over the detected barcodes
        for barcode in barcodes:
                # extract the bounding box location of the barcode and draw the
                # bounding box surrounding the barcode on the image
                (x, y, w, h) = barcode.rect
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # the barcode data is a bytes object so if we want to draw it on
                # our output image we need to convert it to a string first
                attendance = barcode.data.decode("utf-8")

        try:
                if attendance != '': #if attendance found break loop
                        print('Attendance link found: ' + attendance)
                        break
        except:
                sleep(5)
                continue

#login mmu
pg.hotkey('ctrl','t') #open new tab
sleep(1)
pg.typewrite(attendance+'\n') #go to attendance link
sleep(3)
pg.click(633,400) #sign attendance
sleep(5)
pg.hotkey('ctrl','w') #close attendance tab

#after 2 hours, stop recording, close chrome and program
while True:
    if hours >= 2:
        sleep(1)
        pg.hotkey('ctrl','w') #close chrome
        sleep(1)
        pg.hotkey('f1') #stop recording
        sys.exit()
