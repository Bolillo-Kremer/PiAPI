# PiAPI
##### [Bolillo Kremer](https://youtube.com/BolilloKremer?https://www.youtube.com/BolilloKremer?sub_confirmation=1)

## Overview
PiAPI is a user friendly web server that runs on Python or [Node.js] (https://nodejs.org) that allows you to interface with your raspberry pi's gpio pins from anywhere using virtually any language! This can be extremely useful to developers in many situations, but due to this application running off of a web server, using this application for percise timing may be an issue for some users.

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
In your raspberry pi terminal, download the install script for the API version that you want to run

Node API
```sh
$ sudo wget https://raw.githubusercontent.com/Bolillo-Kremer/PiAPI/master/Node/install.sh
```

Python API
```sh
$ sudo wget https://raw.githubusercontent.com/Bolillo-Kremer/PiAPI/master/Python/install.sh
```

Next, make this script executable with this command
```sh
$ sudo chmod +x install.sh
```
Finally, run the install script with this command
```sh
$ sudo bash install.sh
```
#### Using PiAPI in other languages

There is currently only one library available for .Net languages. You can view that project [here](https://github.com/Bolillo-Kremer/PiAPI.NET) or download the nuget package in visual studio using the following command in the package manager terminal.
```
PM Install-Package PiAPI
```
