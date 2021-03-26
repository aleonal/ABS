import pyautogui
from PIL import Image
import os, os.path

print("SCRIPT IS RUNNING\n")
pyautogui.PAUSE = 1.5
x, y = pyautogui.locateCenterOnScreen(os.path.join('/home/kali/Desktop','terminalScreenshotRedDot.png'), confidence=0.5)
pyautogui.click(x,y)
pyautogui.typewrite('ping 8.8.8.8')
pyautogui.typewrite(['enter'])
