import pyautogui
from PIL import Image
import os, os.path

pyautogui.PAUSE = 2.0
x, y = pyautogui.locateCenterOnScreen(os.path.join('/home/kali/Desktop','terminalScreenshotRedDot.png'), confidence=0.5)
pyautogui.click(x,y)
pyautogui.typewrite('wget google.com')
pyautogui.typewrite(['enter'])
pyautogui.typewrite('ping google.com')
pyautogui.typewrite(['enter'])
pyautogui.hotkey('ctrl', 'c')
pyautogui.PAUSE = 2.0
x, y = pyautogui.locateCenterOnScreen(os.path.join('/home/kali/Desktop','kaliScreenshot.png'), confidence=0.5)
pyautogui.click(x,y)
pyautogui.PAUSE = 2.0
x, y = pyautogui.locateCenterOnScreen(os.path.join('/home/kali/Desktop','kaliLinuxScreenshot.png'), confidence=0.5)
pyautogui.click(x,y)
pyautogui.keyDown('alt')
pyautogui.typewrite(['tab'])
pyautogui.keyUp('alt')
x, y = pyautogui.locateCenterOnScreen(os.path.join('/home/kali/Desktop','ipAddressScreenshot.png'), confidence=0.5)
pyautogui.doubleClick(x,y)
x, y = pyautogui.locateCenterOnScreen(os.path.join('/home/kali/Desktop','ipAddressScreenshot.png'), confidence=0.5)
pyautogui.rightClick(x,y)
pyautogui.PAUSE = 2.0
x, y = pyautogui.locateCenterOnScreen(os.path.join('/home/kali/Desktop','copyScreenshot.png'), confidence=0.5)
pyautogui.click(x,y)
pyautogui.PAUSE = 2.0
x, y = pyautogui.locateCenterOnScreen(os.path.join('/home/kali/Desktop','browserScreenshot.png'), confidence=0.5)
pyautogui.click(x,y)
pyautogui.PAUSE = 2.0
x, y = pyautogui.locateCenterOnScreen(os.path.join('/home/kali/Desktop','browserBarScreenshot.png'), confidence=0.5)
pyautogui.click(x,y)
pyautogui.keyDown('shift')
pyautogui.hotkey('home', 'ctrl')
pyautogui.typewrite(['enter'])
pyautogui.keyUp('shift')
