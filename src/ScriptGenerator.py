import pyautogui
from PIL import Image
import os, os.path
import json

class ScriptGenerator():

    def __init__(self, script_name):
        self.generate_script(script_name)

    def generate_script(self, script_name):

        script = "import pyautogui\nfrom PIL import Image\nimport os, os.path\nbreakpoint()\n\n"
        validator = []

        with open(script_name) as f:
            data = json.load(f)
            for d in data:
                print(d)
                try:
                    if d["Type"] == "clicks_id":
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
                        d["v"] = "action"
                        validator.append(d)
                    elif d["Type"] == "keypresses_id":
                        if d["Subtype"] == "type":
                            script += "pyautogui.typewrite('" + d["Attributes"] + "')\n"
                        elif d["Subtype"] == "command":
                            script += "pyautogui.typewrite(['" + d["Attributes"] + "'])\n"
                        elif d["Subtype"] == "hotkey":
                            script += "pyautogui.hotkey(" + d["Attributes"] + ")\n"
                        elif d["Subtype"] == "keyDown":
                            script += "pyautogui.keyDown('" + d["Attributes"] + "')\n"
                        elif d["Subtype"] == "keyUp":
                            script += "pyautogui.keyUp('" + d["Attributes"] + "')\n" 
                        d["v"] = "action"
                        validator.append(d)
                    else:
                        d["v"] = "observation"
                        validator.append(d)
                    #script += "pyautogui.PAUSE = 2\n"
                except Exception as e:
                    print(d["Type"], " error ", e)
                    print(d["Attributes"])
                    print(d["Attributes"]["x"])
                
        p = open(script_name.replace(".json", ".py"), 'w')
        p.write(script)
        p.close()

        #TODO: Figure out how obs need to delivered to the runner/validator
        with open(script_name.replace(".json", "Validator.json"), "w") as obsFile:
            json.dump(validator, obsFile, indent=2)
        

if __name__ == "__main__":
    ScriptGenerator(r"C:\Users\valma\OneDrive\Desktop\ABS\Test\TestBuilder\scriptGenTest1.json")