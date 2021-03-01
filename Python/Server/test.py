import json
import os
import sys 

path = os.path.abspath(os.path.dirname(sys.argv[0]))

settings = json.load(open(path + "/Settings.json"))

for pin in settings['defaultPins']:
    print(pin)