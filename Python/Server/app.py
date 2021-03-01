import json
import os
import sys
import traceback
import RPi.GPIO as GPIO
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api

path = os.path.abspath(os.path.dirname(sys.argv[0]))

#Setting Up
setDirections = {"in": GPIO.IN, "out": GPIO.OUT}
stateFunctions = {"in": GPIO.input, "out": GPIO.output}
gpioStates = {0: GPIO.LOW, 1: GPIO.HIGH}
pull = {"up": GPIO.PUD_UP, "down": GPIO.PUD_DOWN, "none": GPIO.PUD_OFF}
edge = {"rising": GPIO.RISING, "falling": GPIO.FALLING, "both": GPIO.BOTH }
boardTypes = {"bcm": GPIO.BCM, "board": GPIO.BOARD}

settings = json.load(open(path + "/Settings.json"))
port = int(settings["port"])
host = settings["host"]
ios = {}

#Initiates default pins. 
for pinData in settings['defaultPins']:
    init_pin(pinData)

GPIO.setmode(boardTypes[settings["mode"]])


#Creates Server
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

#Gets a setting from the settings json
class GetSetting(Resource):
    def post(self):
        setting = request.get_data(as_text=True)
        print(setting)
        try:
            return settings[setting]
        except Exception as e:
            error = {}
            error["message"] = str(e)
            error["stack"] = "".join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))         
            return error
api.add_resource(GetSetting, '/GetSetting')    

#Sets a setting and saves it to Settings.json
class SetSetting(Resource):
    def post(self):
        data = request.get_data(as_text=True)
        print(data)
        try:
            data = json.loads(data)
            if (data["setting"] in settings):
                settings[data["setting"]] = json.loads(data["val"])
                json.dump(settings, open(path + "/Settings.json", "w"), indent=4)
                return "Settings updated"
            else:
                return "Setting name " + data["setting"] + "does not exist"
        except Exception as e:
            error = {}
            error["message"] = str(e)
            error["stack"] = "".join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))         
            return error
api.add_resource(SetSetting, '/SetSetting')

def init_pin(data):
    pin = int(data["pin"])
    ios[pin] = {}
    ios[pin]["pin"] = pin
    ios[pin]["direction"] = setDirections[data["direction"]]
    ios[pin]["interact"] = stateFunctions[data["direction"]]
    
    if "edge" in data:
        ios[pin]["edge"] = edge[data["edge"]]
        if "edgeTimeout" in data:
            ios[pin]["edgeTimeout"] = int(data["edgeTimeout"])
        else:
            ios[pin]["edgeTimeout"] = None
    else:
        ios[pin]["edge"] = None

    if "pull" in data:
        ios[pin]["pull"] = pull[data["pull"]]
    else:
        ios[pin]["pull"] = pull["none"] 

    if "state" in data:
        ios[pin]["state"] = gpioStates[int(data["state"])]
    else:
        ios[pin]["state"] = gpioStates[0]

    if ios[pin]["direction"] == GPIO.OUT:
        GPIO.setup(pin, ios[pin]["direction"], pull_up_down = ios[pin]["pull"], initial=ios[pin]["state"])
    else:
        GPIO.setup(pin, ios[pin]["direction"], pull_up_down = ios[pin]["pull"])

    if "edge" in data:
        GPIO.wait_for_edge(pin, edge[data["edge"]], timeout = ios[pin]["edgeTimeout"])

    return pin

#Imports a given pin
class InitPin(Resource):
    def post(self):
        data = request.get_data(as_text=True)
        print(data)
        try:
            data = json.loads(data)
            pin = init_pin(data)
            return ios[pin]["state"]

        except Exception as e:
            error = {}
            error["message"] = str(e)
            error["stack"] = "".join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))         
            return error


api.add_resource(InitPin, '/InitPin')

#Returns the state of a given pin. If given "*", returns JSON of all pin states
class GetState(Resource):
    def post(self):
        pin = request.get_data(as_text=True)
        print(pin)
        try:
            if pin == "*":
                states = {}
                pins = list(ios.keys())
                for iopin in pins:
                    states[iopin] = ios[iopin]["state"]
                return states
            else:
                if (int(pin) in ios):
                    return ios[int(pin)]["state"]
                else:
                    return "Error: Pin " + pin + " not initialized"
        except Exception as e:
            error = {}
            error["message"] = str(e)
            error["stack"] = "".join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))         
            return error
api.add_resource(GetState, '/GetState')

#Returns a JSON of all active pins
class ActivePins(Resource):
    def get(self):
        try:
            print("Active Pins")
            activePins = {}

            for pin in list(ios.keys()):
                activePins[pin] = ios[pin]["direction"]

            return activePins

        except Exception as e:
            error = {}
            error["message"] = str(e)
            error["stack"] = "".join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))         
            return error
api.add_resource(ActivePins, '/ActivePins')

#Sets the state of a given pin. If given "*" sets the state of all pins
class SetState(Resource):
    def post(self):
        data = request.get_data(as_text=True)
        print(data)
        try:
            data = json.loads(data)
            if data["pin"] == "*":
                pins = list(ios.keys())
                message = {}
                message["success"] = list()
                message["failed"] = list()

                for pin in pins:
                    if ios[pin]["direction"] == GPIO.OUT:
                        try:
                            if int(data["state"]) == -1:
                                ios[pin]["interact"](pin, not bool(ios[pin]["state"]))
                                ios[pin]["state"] = int(not bool(ios[pin]["state"]))
                                message["success"].append(pin)
                            else:
                                ios[pin]["interact"](pin, gpioStates[int(data["state"])])
                                ios[pin]["state"] = gpioStates[int(data["state"])]
                                message["success"].append(pin)
                        except Exception as e:
                            fail = {}
                            fail["pin"] = pin
                            fail["exception"] = str(e)
                            message["failed"].append(fail)
                
                return message
            else:
                pin = int(data["pin"])
                if (pin in ios):
                    if ios[pin]["direction"] == GPIO.OUT:
                        if (int(data["state"]) == -1):
                            ios[pin]["interact"](pin, not bool(ios[pin]["state"]))
                            ios[pin]["state"] = int(not bool(ios[pin]["state"]))
                        else:
                            ios[pin]["interact"](pin, gpioStates[int(data["state"])])
                            ios[pin]["state"] = gpioStates[int(data["state"])]
                        return ios[pin]["state"]
                    else:
                        return "Error: Can't set state of pin " + str(pin) + " because it is set to input"
                else:
                    return "Error: Pin " + str(pin) + " not initialized"

        except Exception as e:
            error = {}
            error["message"] = str(e)
            error["stack"] = "".join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))         
            return error
api.add_resource(SetState, '/SetState')

#Unexports all pins
class CleanExit(Resource):
    def get(self):
        try:
            print('Clean Exit')
            GPIO.cleanup()
            ios = {}
            return "Clean Exit"
        except Exception as e:
            error = {}
            error["message"] = str(e)
            error["stack"] = "".join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))         
            return error
api.add_resource(CleanExit, '/CleanExit')

#Unexports a given pin
class Unexport(Resource):
    def get(self):
        return "This function is currenty unavailable for PiAPI Python. Please consider switching to the PiAPI Node"
api.add_resource(Unexport, '/Unexport')

#Executes a given terminal command
class Command(Resource):
    def post(self):
        data = request.get_data(as_text=True)
        print(data)
        try:
            command = os.system(data)
            return command
        except Exception as e:
            error = {}
            error["message"] = str(e)
            error["stack"] = "".join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))         
            return error
api.add_resource(Command, '/Command')
            
if __name__ == "__main__":
    app.run(debug=settings["debug"], port=port, host=host)
