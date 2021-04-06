import pyautogui
from PIL import Image
import os, os.path

pyautogui.PAUSE = 1
print("PAUSE 1 second")

pyautogui.leftClick(179,1068)
print("LeftClick")
pyautogui.typewrite('cmd')
pyautogui.typewrite(['enter'])
pyautogui.typewrite('cd oneDrive\Desktop')
pyautogui.typewrite(['enter'])
pyautogui.typewrite('test.txt')
pyautogui.typewrite(['enter'])
pyautogui.hotkey("ctrl", "a")
pyautogui.hotkey("ctrl", "c")
pyautogui.leftClick(179,1068)
pyautogui.typewrite('cmd')
pyautogui.typewrite(['enter'])
pyautogui.typewrite('git clone ')
pyautogui.hotkey("ctrl","v")
pyautogui.PAUSE = 5
pyautogui.typewrite(['enter'])
pyautogui.PAUSE = 1
pyautogui.typewrite('cd PracticumDemo')
pyautogui.typewrite(['enter'])
pyautogui.typewrite('python PracticumDemo.py')
pyautogui.typewrite(['enter'])
