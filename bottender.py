import pyautogui as pg
import re
import os
from time import sleep

def getLink(): #get the line of selected google meet link
    try:
        linkSelect = int(input('Please enter the digit of your selected google meet link; eg: 1,2,3,...\n'))
    except ValueError:
        print('Error, please enter only digits')
        getLink()
    return linkSelect

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
meetlink = os.path.join(THIS_FOLDER, 'meetlink.txt')

i = 0
with open(meetlink, 'r') as fp:
    for lines in (fp.read().split('\n'))[1:]: #output selection of meet link
        i += 1
        print(str(i) + ': ' + lines)

with open(meetlink, 'r') as fp:
    mo = re.findall('https.*', fp.read())
link = mo[getLink()-1] #store google meet link to 'link' variable

pg.hotkey('winleft') #press windows key on keyboard
sleep(1)
pg.typewrite('chrome\n',0.1) #type in chrome in search bar and enter

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

#scan for attendance QR code
#login mmu
#stop recording after 2 hours
#close program
