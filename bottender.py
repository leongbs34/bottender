import pyautogui as pg
import re

def getLink(): #get the line of selected google meet link
    try:
        linkSelect = input('Please enter the digit of your selected google meet link; eg: 1,2,3,...')
        
    except ValueError:
        print('Error, please enter only digits')
        getLink()
    return int(linkSelect)


pg.hotkey('winleft') #press windows key on keyboard

pg.typewrite('chrome\n') #type in chrome in search bar and enter

fp = open('meetlink.txt', r+)#line to read google meet link
for lines in fp.read().split('\n'): #output selection of meet link
    i = 1
    print(i + ': ' + lines+1)
    i += 1
linkRegex = re.compile(r'https.*')
mo = linkRegex.findall(fp.read())
link = mo[getLink()-1] #store google meet link to 'link' variable
print(link)




#pg.typewrite(gmeet) #enter link from meetlink.txt

#pg.hotkey('winkey','up') #fullscreen google chrome