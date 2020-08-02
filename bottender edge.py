import pyautogui as pg
import sys
import re
from desktopmagic.screengrab_win32 import getScreenAsImage 
import os
import glob
from time import time
from time import sleep
from pyzbar import pyzbar
import imutils
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

start_time = time() #start timer

i = 0
with open(meetlink, 'r') as fp:
    for lines in (fp.read().split('\n'))[1:]: #output selection of meet link
        i += 1
        print(str(i) + ': ' + lines)

with open(meetlink, 'r') as fp:
    mo = re.findall('https.*', fp.read())
link = mo[getLink()-1] #store google meet link to 'link' variable

print('''Bot will take control of your computer for awhile, please do not press anything until mention
Beginning in 3 seconds...''')
sleep(3)

print('Bot started')
pg.hotkey('winleft') #press windows key on keyboard
sleep(1)
pg.typewrite('edge\n',0.1) #type in edge in search bar and enter
sleep(5)
pg.click(662,53) #click on url 
pg.typewrite(link + '\n') #enter link from meetlink.txt
pg.hotkey('winkey','up') #fullscreen google edge
sleep(5)
pg.hotkey('ctrl','d') #mute mic
sleep(1)
pg.hotkey('ctrl','e') #hide cam

sleep(3)
join = pg.locateOnScreen('join.png', confidence=0.9)
pg.click(join[0], join[1]) #join classroom
sleep(1)
chat = pg.locateOnScreen('chat.png', confidence=0.9)
pg.click(chat[0], chat[1]) #show chat

#open obs
pg.hotkey('winleft') #press windows key on keyboard
sleep(1)
pg.typewrite('obs\n',0.1)
sleep(5)

#start recording , requires start recording and stop recording hotkey
hotkeyRec = 'f1'
pg.hotkey(hotkeyRec)
sleep(1)
pg.hotkey('alt','\t') #alt tab into edge

print('''Scanning for QR code...
Bot control paused until QR code is found on screen''')

#QR scanner
while True:
        entireScreen = getScreenAsImage()
        entireScreen.save('ss.png', format='png') #take a screenshot
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
                hours = (time() - start_time ) / 3600
                if attendance != '': #if attendance found break loop
                        print('Attendance link found: ' + attendance)
                        print('Bot control beginning in 3 seconds, please do not touch anything until you are told')
                        sleep(3)
                        break

                if hours >= 2:
                    print('Attendance link not found after 2h')
                    sleep(1)
                    pg.hotkey('ctrl','w') #close edge
                    sleep(1)
                    pg.hotkey(hotkeyRec) #stop recording
                    sys.exit()
                    
        except:
                sleep(5)
                continue

#login mmu
pg.hotkey('ctrl','t') #open new tab
sleep(1)
pg.typewrite(attendance+'\n') #go to attendance link
sleep(3)
pg.press('enter') #sign attendance
sleep(5)
pg.hotkey('ctrl','w') #close attendance tab
print('Attendance signed, you may use your computer now, recording will stop after 2 hours')

#after 2 hours, stop recording, close edge and program
while True:
    hours = (time() - start_time ) / 3600
    if hours >= 2:
        print(hours)
        sleep(1)
        pg.hotkey('ctrl','w') #close edge
        sleep(1)
        pg.hotkey(hotkeyRec) #stop recording
        sys.exit()
