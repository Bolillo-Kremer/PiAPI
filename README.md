# PiAPI
##### [Bolillo Kremer](https://youtube.com/BolilloKremer?https://www.youtube.com/BolilloKremer?sub_confirmation=1)

![PiAPI icon](https://raw.githubusercontent.com/Bolillo-Kremer/PiAPI/master/PiAPI.png)

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
In your raspberry pi terminal, simply run the install script for the API version that you want!
If [cURL](https://curl.haxx.se/) is already installed, you can skip the first command.

Install cURL
```sh
$ sudo apt-get install php-curl
```

Node API
```sh
$ bash <(curl -s https://raw.githubusercontent.com/Bolillo-Kremer/PiAPI/master/Node/install.sh)
```

Python API
```sh
$ bash <(curl -s https://raw.githubusercontent.com/Bolillo-Kremer/PiAPI/master/Python/install.sh)
```

#### Available PiAPI Client Libraries
- [PiAPI.NET](https://github.com/Bolillo-Kremer/PiAPI.NET)
- [PiAPI Java](https://github.com/Bolillo-Kremer/PiAPI-Java)
- PiAPI Python Client (In progress)
- PiAPI JavaScript Client (In progress)
- PiAPI C++ (In Progress)
