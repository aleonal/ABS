import pyautogui
from PIL import Image
import os, os.path
import json

class ScriptGen2():

    def __init__(self, script_name):
        # Initialize python file contents
        self.script = "import pyautogui\nfrom PIL import Image\nimport os, os.path\n\n"
        # Initailize validator json file
        self.validator = []
        # Use Builder dependencies file to create script
        self.generate_script(script_name)

    def generate_script(self, script_name):
        # open dependencies file from builder
        with open(script_name) as f:
            data = json.load(f)
            # traverse for event in data and for child in event["children"]
            for event in data:
                # if its a click do something
                if event["Type"] == "clicks_id" or event["Type"] == "timed_id":
                    self.click(event)
                # if its a keypress do something
                elif event["Type"] == "keypresses_id":
                    self.keypress(event)
                # if its an observation do something
                else:
                    event["v"] = "observation"
                # iterate through children before moving on to the next event
                for child in event["Children"]:
                    if "Children" not in child:
                        child["Children"] = []
                    # if its a click do something
                    if child["Type"] == "clicks_id" or child["Type"] == "timed_id":
                        self.click(child)
                    # if its a keypress do something
                    elif child["Type"] == "keypresses_id":
                        self.keypress(child)
                    # if its an observation do something
                    else:
                        child["v"] = "observation"
                # Only append root events in validator list since children events already present within root events
                self.validator.append(event)

        # Create the python file
        p = open(script_name.replace(".json", ".py"), "w")
        p.write(self.script)
        p.close()

        # Create validator file
        with open(script_name.replace(".json", "Validator.json"), "w") as vFile:
            json.dump(self.validator, vFile, indent=2)

    def click(self, c):
        # load coordinates
        coordinates = json.loads(c["Attributes"])
        x, y = coordinates["x"], coordinates["y"]
        # leftClick
        if c["Subtype"] == "leftClick":
            self.script += "pyautogui.leftClick({},{})\n".format(x,y)
        # rightClick
        elif c["Subtype"] == "rightClick":
            self.script += "pyautogui.rightClick({},{})\n".format(x,y)
        # doubleClick
        elif c["Subtype"] == "doubleClick":
            self.script += "pyautogui.doubleClick({},{})\n".format(x,y)
        # add validator key
        c["v"] = "action"

    def keypress(self, k):
        # type
        if k["Subtype"] == "type":
            self.script += "pyautogui.typewrite('" + k["Attributes"] + "')\n"
        # command
        elif k["Subtype"] == "command":
            self.script += "pyautogui.typewrite(['" + k["Attributes"] + "'])\n"
        # hotkey
        elif k["Subtype"] == "hotkey":
            removeSpace = k["Attributes"].strip()
            hotkeys = removeSpace.split(",")
            hk1 = hotkeys[0]
            hk2 = hotkeys[1]
            self.script += "pyautogui.hotkey('" + hk1 + "', '" + hk2 + "')\n"
        # keyDown
        elif k["Subtype"] == "keyDown":
            self.script += "pyautogui.keyDown('" + k["Attributes"] + "')\n"
        # keyUp
        elif k["Subtype"] == "keyUp":
            self.script += "pyautogui.keyUp('" + k["Attributes"] + "')\n"
        k["v"] = "action"


if __name__ == "__main__":
    ScriptGen2(r"C:\Users\valma\OneDrive\Desktop\lastDemoProject\fixSG.json")