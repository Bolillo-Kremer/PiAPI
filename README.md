# PiAPI
##### [Bolillo Kremer](https://youtube.com/BolilloKremer?https://www.youtube.com/BolilloKremer?sub_confirmation=1)

<div align="center">
  <img src="https://raw.githubusercontent.com/Bolillo-Kremer/PiAPI/master/PiAPI.png" alt="PiAPI icon" width="300px" height="300px">
</div>

## Overview
PiAPI is a user friendly web server that runs on Python or [Node.js](https://nodejs.org) that allows you to interface with your raspberry pi's gpio pins from anywhere using virtually any language! This can be extremely useful to developers looking to control multiple Pi's at once with just one application and for beginners looking to learn raspberry pi with any language.

For updates on this project and other other entertainging coding projects, please subscribe to my YouTube channel, [Bolillo Kremer](https://youtube.com/BolilloKremer?https://www.youtube.com/BolilloKremer?sub_confirmation=1). 

## Current Features!
  - Reading gpio states
  - Setting gpio states
  - Executing terminal commands
  
## Future Goals
 - Reading serial data
 - More code libraries for other languages


## How to use
#### Installing PiAPI on your Raspberry Pi

Most operating systems for the raspberry pi come with [cURL](https://curl.haxx.se/) already installed, but if it isn't you can install it with this command.

Install cURL
```sh
$ sudo apt-get install php-curl
```
Now you're ready to install PiAPI! Simply choose if you want to run PiAPI on Node.js or Python and paste the corresponding command into your terminal.

(NOTE) Some pi's may have trouble downloading the Node API. If you are unsure if Node.js is compatible with your pi, choose the Python API.

Python API
```sh
$ bash <(curl -s https://raw.githubusercontent.com/Bolillo-Kremer/PiAPI/master/Python/install.sh)
```

Node API
```sh
$ bash <(curl -s https://raw.githubusercontent.com/Bolillo-Kremer/PiAPI/master/Node/install.sh)
```

## Settings
You can change certain API settings from the Settings.json in the server directory of PiAPI

### port
The port that PiAPI will run on

### mode
The pin mode of the raspberry pi (Python API only)

### debug
Choose whether or not to run in debug mode

### defaultPins
This setting is an array of pin objects that PiAPI will initialize on boot. They can be set up just like how you would initialize a pin.

```json
{
  "defaultPins": [
    {"pin": 1, "direction": "out"},
    {"pin": 2, "direction": "in", "edge": "falling"}
  ]
}
```

#### Available PiAPI Client Libraries
- [PiAPI.NET](https://github.com/Bolillo-Kremer/PiAPI.NET)
- [PiAPI Java](https://github.com/Bolillo-Kremer/PiAPI-Java)
- [PiAPI Python Client](https://github.com/Bolillo-Kremer/PiAPI-Python_Client)
- [PiAPI JavaScript Client](https://github.com/Bolillo-Kremer/PiAPI-NPM)
- PiAPI C++ (In Progress)
