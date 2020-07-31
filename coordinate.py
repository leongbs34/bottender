import pyautogui #use to simulate mouse and keyboard movement
from time import sleep
pyautogui.PAUSE = 1 #pause for 1 sec before executing pyautogui function call
sleep(5) #wait for 5 sec

x,y = pyautogui.position() #inputs the current mouse position after 5 sec
print(x,y) #prints out the mouse position

