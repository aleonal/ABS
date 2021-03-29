import pyautogui
from PIL import Image
import os, os.path

pyautogui.leftClick(197,1070)
pyautogui.PAUSE = 2
pyautogui.PAUSE = 2
pyautogui.PAUSE = 2
pyautogui.typewrite('cmd')
pyautogui.PAUSE = 2
pyautogui.typewrite(['enter'])
pyautogui.PAUSE = 3
pyautogui.PAUSE = 2
pyautogui.typewrite('cd oneDrive\Desktop')
pyautogui.PAUSE = 2
pyautogui.typewrite(['enter'])
pyautogui.PAUSE = 3
pyautogui.PAUSE = 2
pyautogui.typewrite('test.txt')
pyautogui.PAUSE = 2
pyautogui.typewrite(['enter'])
pyautogui.PAUSE = 3
pyautogui.PAUSE = 2
pyautogui.hotkey("ctrl","a")
pyautogui.PAUSE = 2
pyautogui.hotkey("ctrl","c")
pyautogui.PAUSE = 2
pyautogui.leftClick(188,1064)
pyautogui.PAUSE = 2
pyautogui.typewrite('cmd')
pyautogui.PAUSE = 2
pyautogui.typewrite(['enter'])
pyautogui.PAUSE = 3
pyautogui.PAUSE = 2
pyautogui.typewrite('git clone ')
pyautogui.PAUSE = 2
pyautogui.hotkey("ctrl", "v")
pyautogui.PAUSE = 2
pyautogui.typewrite(['enter'])
pyautogui.PAUSE = 3
pyautogui.PAUSE = 2
pyautogui.typewrite('cd PracticumDemo')
pyautogui.PAUSE = 2
pyautogui.typewrite(['enter'])
pyautogui.PAUSE = 3
pyautogui.PAUSE = 2
pyautogui.typewrite('python PracticumDemo.py')
pyautogui.PAUSE = 2
pyautogui.typewrite(['enter'])
pyautogui.PAUSE = 3
pyautogui.PAUSE = 2
