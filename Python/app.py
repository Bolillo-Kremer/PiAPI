import json
import sys
import RPi.GPIO as GPIO
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api

#Setting Up
setDirections = {"in": GPIO.IN, "out": GPIO.OUT}
stateFunctions = {"in": GPIO.input, "out": GPIO.output}
gpioStates = {0: GPIO.LOW, 1: GPIO.HIGH}
pull = {"up": GPIO.PUD_UP, "down": GPIO.PUD_DOWN}
edge = {"rising": GPIO.RISING, "falling": GPIO.FALLING, "both": GPIO.BOTH }
boardTypes = {"bcm": GPIO.BCM, "board": GPIO.BOARD}

settings = json.load(open("Settings.json"))
port = int(settings["port"])
ios = {}

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
            return "Error: " + str(e)
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
                json.dump(settings, open("Settings.json", "w"), indent=4)
                return "Settings updated"
            else:
                return "Setting name " + data["setting"] + "does not exist"
        except Exception as e:
            return "Error: " + str(e)
api.add_resource(SetSetting, '/SetSetting')

class InitPin(Resource):
    def post(self):
        data = request.get_data(as_text=True)
        print(data)
        try:
            data = json.loads(data)

            ios[data["pin"]] = {}
            ios[data["pin"]]["pin"] = data["pin"]
            ios[data["pin"]]["direction"] = data["direction"]
            ios[data["pin"]]["interact"] = stateFunctions[data["direction"]]
            
            if "edge" in data:
                ios[data["pin"]]["edge"] = edge[data["edge"]]
                if "edgeTimeout" in data:
                    ios[data["pin"]]["edgeTimeout"] = int(data["edgeTimeout"])
                else:
                    ios[data["pin"]]["edgeTimeout"] = None
            else:
                ios[data["pin"]]["edge"] = None

            if "pull" in data:
                ios[data["pin"]]["pull"] = pull[data["pull"]]
            else:
                ios[data["pin"]]["pull"] = None   

            if "state" in data:
                ios[data["pin"]]["state"] = gpioStates[data["state"]]
            else:
                ios[data["pin"]]["state"] = None
            
            GPIO.setup(data["pin"], setDirections[data["direction"]], pull_up_down = ios[data["pin"]]["pull"], initial=ios[data["pin"]]["state"])

            if "edge" in data:
                GPIO.wait_for_edge(data["pin"], edge[data["edge"]], timeout = ios[data["pin"]]["edgeTimeout"])

            return "Initiated pin " + data["pin"]

        except Exception as e:
            return "Error: " + str(e)
api.add_resource(InitPin, '/InitPin')

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
                return iopin
            else:
                if (pin in ios):
                    return ios[pin]["state"]
                else:
                    return "Error: Pin " + pin + " not initialized"
        except Exception as e:
            return "Error: " + str(e)
api.add_resource(GetState, '/GetState')

class ActivePins(Resource):
    def get(self):
        try:
            print("Active Pins")
            activePins = {}

            for pin in list(ios.keys()):
                activePins[pin] = ios[pin]["direction"]

            return activePins

        except Exception as e:
            return "Error: " + str(e)
api.add_resource(ActivePins, '/ActivePins')

class SetState(Resource):
    def post(self):
        data = request.get_data(as_text=True)
        print(data)
        try:
            if data["pin"] == "*":
                data = json.loads(data)
                pins = list(ios.keys())
                message = {}
                message["success"] = list()
                message["failed"] = list()

                for pin in pins:
                    if ios[pin]["direction"] == setDirections["out"]:
                        try:
                            ios[pin]["interact"](pin, gpioStates[data["state"]])
                            ios[pin]["state"] = gpioStates[data["state"]]
                            message["success"].append(pin)
                        except Exception as e:
                            fail = {}
                            fail["pin"] = pin
                            fail["exception"] = str(e)
                            message["failed"].append(fail)
                
                return message
            else:
                data = json.loads(data)
                if (data["pin"] in ios):
                    if ios[data["pin"]]["direction"] == "out":
                        ios[data["pin"]]["interact"](data["pin"], gpioStates[data["state"]])
                        ios[data["pin"]]["state"] = gpioStates[data["state"]]
                        return data["state"]
                    else:
                        return "Error: Can't set state of pin " + data["pin"] + " because it is set to input"
                else:
                    return "Error: Pin " + data["pin"] + " not initialized" 

        except Exception as e:
            return "Error: " + str(e)
api.add_resource(SetState, '/SetState')


class CleanExit(Resource):
    def get(self):
        try:
            print('Clean Exit')
            GPIO.cleanup()
            ios = {}
            return "Clean Exit"
        except Exception as e:
            "Error: " + str(e)
api.add_resource(CleanExit, '/CleanExit')

class Unexport(Resource):
    def get(self):
        return "This function is currenty unavailable for the Python API. Please consider switching to the Node API"
api.add_resource(Unexport, '/Unexport')









if __name__ == "__main__":
    app.run(debug=settings["debug"], port=port)