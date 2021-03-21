import pyautogui
from PIL import Image
import os, os.path
import json

# TODO: Get path from project controller
path = "/home/kali/Desktop"
# TODO: Get script name from project controller
script_name = "sampleScriptGoogle.json"

script = "import pyautogui\nfrom PIL import Image\nimport os, os.path\n\n"

with open(os.path.join(path,script_name)) as f:
    data = json.load(f)
    for d in data:
        if d["type"] == "leftClick":
            script += "pyautogui.PAUSE = " + str(d["time"]) + "\n"
            script += "x, y = pyautogui.locateCenterOnScreen(os.path.join('" + path + "','" + d["content"] + "'), confidence=0.5)\n"
            script += "pyautogui.click(x,y)\n"
        elif d["type"] == "rightClick":
            script += "x, y = pyautogui.locateCenterOnScreen(os.path.join('" + path + "','" + d["content"] + "'), confidence=0.5)\n"
            script += "pyautogui.rightClick(x,y)\n"
        elif d["type"] == "doubleClick":
            script += "x, y = pyautogui.locateCenterOnScreen(os.path.join('" + path + "','" + d["content"] + "'), confidence=0.5)\n"
            script += "pyautogui.doubleClick(x,y)\n"
        elif d["type"] == "typewrite":
            script += "pyautogui.typewrite('" + d["content"] + "')\n"
        elif d["type"] == "typewriteCommand":
            script += "pyautogui.typewrite(['" + d["content"] + "'])\n"
        elif d["type"] == "hotkey":
            script += "pyautogui.hotkey(" + d["content"] + ")\n"
        elif d["type"] == "keyDown":
            script += "pyautogui.keyDown('" + d["content"] + "')\n"
        elif d["type"] == "keyUp":
            script += "pyautogui.keyUp('" + d["content"] + "')\n" 
        

p = open(os.path.join(path, script_name.replace('.json', '.py')), 'w')
p.write(script)
p.close()

