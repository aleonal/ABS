import pyautogui
from PIL import Image
import os, os.path

pyautogui.PAUSE = 2.5
pyautogui.typewrite(['win'])
pyautogui.typewrite('cmd')
pyautogui.typewrite(['enter'])
pyautogui.typewrite('ping google.com')
pyautogui.PAUSE = 5
pyautogui.hotkey("ctrl", "c")
pyautogui.PAUSE = 2.5
pyautogui.doubleClick(163,186)
pyautogui.hotkey("ctrl", "c")
pyautogui.leftClick(612,1071)
pyautogui.PAUSE = 5
pyautogui.hotkey("ctrl", "v")
pyautogui.typewrite(['enter'])
pyautogui.typewrite('i am agent build system')
