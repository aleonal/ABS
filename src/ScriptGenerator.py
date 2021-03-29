import pyautogui
from PIL import Image
import os, os.path
import json

class ScriptGenerator():

    def __init__(self, script_name):
        self.generate_script(script_name)
    def generate_script(self, script_name):
        script = "import pyautogui\nfrom PIL import Image\nimport os, os.path\n\n"

        with open(script_name) as f:
            data = json.load(f)
            for d in data:
                if d["Subtype"] == "leftClick":
                    #script += "pyautogui.PAUSE = " + str(d["time"]) + "\n"
                    # Screenshot click: script += "x, y = pyautogui.locateCenterOnScreen(os.path.join('" + path + "','" + d["content"] + "'), confidence=0.5)\n"
                    coordinates = json.loads(d["Attributes"])
                    x, y = coordinates["x"], coordinates["y"]
                    script += "pyautogui.leftClick({},{})\n".format(x,y)
                elif d["Subtype"] == "rightClick":
                    # Screenshot click: script += "x, y = pyautogui.locateCenterOnScreen(os.path.join('" + path + "','" + d["content"] + "'), confidence=0.5)\n"
                    coordinates = json.loads(d["Attributes"])
                    x, y = coordinates["x"], coordinates["y"]
                    script += "pyautogui.rightClick({},{})\n".format(x,y)
                elif d["Subtype"] == "doubleClick":
                    # Screenshot click: script += "x, y = pyautogui.locateCenterOnScreen(os.path.join('" + path + "','" + d["content"] + "'), confidence=0.5)\n"
                    coordinates = json.loads(d["Attributes"])
                    x, y = coordinates["x"], coordinates["y"]
                    script += "pyautogui.doubleClick({},{})\n".format(x,y)
                elif d["Subtype"] == "type":
                    script += "pyautogui.typewrite('" + d["Attributes"] + "')\n"
                elif d["Subtype"] == "command":
                    script += "pyautogui.typewrite(['" + d["Attributes"] + "'])\n"
                    script += "pyautogui.PAUSE = 3\n"
                elif d["Subtype"] == "hotkey":
                    script += "pyautogui.hotkey(" + d["Attributes"] + ")\n"
                elif d["Subtype"] == "keyDown":
                    script += "pyautogui.keyDown('" + d["Attributes"] + "')\n"
                elif d["Subtype"] == "keyUp":
                    script += "pyautogui.keyUp('" + d["Attributes"] + "')\n" 
                script += "pyautogui.PAUSE = 2\n"
                

        p = open(script_name.replace(".json", ".py"), 'w')
        p.write(script)
        p.close()

if __name__ == "__main__":
    ScriptGenerator(r"C:\Users\valma\OneDrive\Desktop\practicum-1\Test\TestRunner\test2.json")