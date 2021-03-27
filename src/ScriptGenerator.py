import pyautogui
#from .ProjectController import ProjectController
from PIL import Image
import os, os.path
import json

class ScriptGenerator():

    def __init__(self, script_name):
        #self.path = ProjectController.get_project_info()["project_directory"]   
        self.generate_script(script_name)
    def generate_script(self, script_name):
        script = "import pyautogui\nfrom PIL import Image\nimport os, os.path\n\n"

        with open(script_name) as f:
            data = json.load(f)
            for d in data:
                if d["Subtype"] == "leftClick":
                    #script += "pyautogui.PAUSE = " + str(d["time"]) + "\n"
                    # Screenshot click: script += "x, y = pyautogui.locateCenterOnScreen(os.path.join('" + path + "','" + d["content"] + "'), confidence=0.5)\n"
                    x, y = int(d["Attributes"][1]), int(d["Attributes"][3])
                    script += "pyautogui.click(x,y)\n"
                elif d["Subtype"] == "rightClick":
                    # Screenshot click: script += "x, y = pyautogui.locateCenterOnScreen(os.path.join('" + path + "','" + d["content"] + "'), confidence=0.5)\n"
                    x, y = int(d["Attributes"][1]), int(d["Attributes"][3])
                    script += "pyautogui.rightClick(x,y)\n"
                elif d["Subtype"] == "doubleClick":
                    # Screenshot click: script += "x, y = pyautogui.locateCenterOnScreen(os.path.join('" + path + "','" + d["content"] + "'), confidence=0.5)\n"
                    x, y = int(d["Attributes"][1]), int(d["Attributes"][3])
                    script += "pyautogui.doubleClick(x,y)\n"
                elif d["Subtype"] == "typewrite":
                    script += "pyautogui.typewrite('" + d["content"] + "')\n"
                elif d["Subtype"] == "typewriteCommand":
                    script += "pyautogui.typewrite(['" + d["Attributes"] + "'])\n"
                elif d["Subtype"] == "hotkey":
                    script += "pyautogui.hotkey(" + d["Attributes"] + ")\n"
                elif d["Subtype"] == "keyDown":
                    script += "pyautogui.keyDown('" + d["content"] + "')\n"
                elif d["Subtype"] == "keyUp":
                    script += "pyautogui.keyUp('" + d["content"] + "')\n" 
                

        p = open(script_name.replace(".json", ".py"), 'w')
        p.write(script)
        p.close()

if __name__ == "__main__":
    ScriptGenerator(r"C:\Users\valma\OneDrive\Desktop\practicum-1\Test\TestRunner\testScript1.json")