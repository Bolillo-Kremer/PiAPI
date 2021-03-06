const http = require('http');
const gpio = require('onoff').Gpio;
const express = require('express');
const fs = require('fs');
const cors = require('cors');
const {exec} = require("child_process");

const settings = JSON.parse(fs.readFileSync('Settings.json'));

//The port that you want the API to run on
const port = Number(settings.port);

//Sets up web server
const app = express();
app.use(cors());
const server = http.createServer(app);

const ios = {};

//Initiates default pins
for (pinData of settings['defaultPins']) {
    initPin(pinData);
}

/**
 * Gets a setting from the setting json
 */
app.post('/GetSetting', (req, res) => {
    req.on('data', (setting) => {
        setting = setting.toString('ascii');
        console.log(setting);
        try {
            res.send(JSON.stringify(settings[setting]));
        }
        catch(e) {
            let error = {
                message: e.toString(),
                stack: Error().stack
            }
            res.send(JSON.stringify(error));
        }
    })
})

/**
 * Sets a setting and saves it to Settings.json
 */
app.post('/SetSetting', (req, res) => {
    req.on('data', (data) => {
        data = data.toString('ascii');
        console.log(data);
        try {
            if (isJSON(data)) {
                data = JSON.parse(data);               
                if (settings.hasOwnProperty(data.setting)) {
                    settings[data.setting] = JSON.parse(data.val);
                    fs.writeFileSync('Settings.json', JSON.stringify(settings, null, '\t'));
                    res.send('Settings updated');
                }
                else {
                    res.send(`Setting name ${data.setting} does not exist`)
                }
            }
            else {
                res.send('Error: Data was not in JSON format and was expected to be');
            }
        }
        catch(e) {
            let error = {
                message: e.toString(),
                stack: Error().stack
            }
            res.send(JSON.stringify(error));
        }
    })
})

/**
 * Returns the state of a given pin. If given "*", returns JSON of all pin states 
 */
app.post('/GetState', (req, res) => {
    req.on('data', (pin) => {
        pin = pin.toString('ascii');
	    console.log(pin);
        try {
            if (pin == '*') {
                let states = {};
                    let pins = Object.keys(ios);
                    for (iopin of pins) {
                        states[iopin] = ios[iopin].pin.readSync().toString();
                    }
                    res.send(JSON.stringify(states));
            }
            else {
                if (ios.hasOwnProperty(pin)) {
                    res.send(ios[pin].pin.readSync().toString());
                }
                else {
                    res.send(`Error: Pin ${pin} not initialized`)
                }
            }          
        }
        catch(e) {
            let error = {
                message: e.toString(),
                stack: Error().stack
            }
            res.send(JSON.stringify(error));
        }
    })
})

/**
 * Returns a JSON of all active pins
 */
app.get('/ActivePins', (req, res) => {
    try {    
        console.log('Active Pins');   
        let activePins = {}

        for (pin of Object.keys(ios)) {
            activePins[pin] = ios[pin].direction;
        }
        res.send(JSON.stringify(activePins));
    }
    catch(e) {
        let error = {
            message: e.toString(),
            stack: Error().stack
        }
        res.send(JSON.stringify(error));
    }
})

/**
 * Sets the state of a given pin. If given "*" sets the state of all pins
 */
app.post('/SetState', (req, res) => {
    req.on('data', (data) => {
        data = data.toString('ascii');
	console.log(data);
	try {
        if (isJSON(data)) {
            data = JSON.parse(data)
            if (data.pin == '*') {
                let pins = Object.keys(ios);
                let successStates = {};
                successStates.success = [];
                successStates.failed = [];
                for (pin of pins) {
                    if (ios[pin].direction == 'out') {
                        try {
                            if (Number(data.state) == -1) {
                                ios[pin].pin.writeSync(ios[pin].pin.readSync() ^ 1);
                            }
                            else {
                                ios[pin].pin.writeSync(data.state);
                            } 
                            successStates.success.push(pin);
                            
                        }       
                        catch (e) {
                            let fail = {};
                            fail.pin = pin;
                            fail.exception = e.toString();
                            successStates.failed.push(fail);
                        }   
                    }             
                }
                res.send(JSON.stringify(successStates));
            }
            else {
                data = JSON.parse(data);
                try {
                    if (ios.hasOwnProperty(data.pin)) {
                        if (ios[data.pin].direction == 'out') {
                            if (Number(data.state) == -1) {
                                ios[data.pin].pin.writeSync(ios[data.pin].pin.readSync() ^ 1);
                            }
                            else {
                                ios[data.pin].pin.writeSync(Number(data.state));
                            }
                            
                            res.send(ios[data.pin].pin.readSync().toString())
                        }
                        else {
                            res.send(`Error: Can't set state of pin ${data.pin} because it is set to input`);
                        }
                    }
                    else {
                        res.send(`Error: Pin ${data.pin} not initialized`);
                    }
                }
                catch(e) {
                    let error = {
                        message: e.toString(),
                        stack: Error().stack
                    }
                    res.send(JSON.stringify(error));
                }

            }
        }
        else {
            res.send('Error: Data was not in JSON format and was expected to be');
        }
	}
	catch(e) {
		let error = {
            message: e.toString(),
            stack: Error().stack
        }
        res.send(JSON.stringify(error));
	}
    })
})

function initPin(data) {
    ios[data.pin].direction = data.direction;
        if (data.hasOwnProperty('edge')){
            ios[data.pin].edge = data.edge;
            if (data.hasOwnProperty('edgeTimeout')) {
                ios[data.pin].options = { debounceTimeout: data.edgeTimeout };
            }
            else {
                ios[data.pin].options = null;
            }
        }
        else {
            ios[data.pin].edge = null;
        } 

    ios[data.pin].pin = new gpio(Number(data.pin), data.direction, ios[data.pin].edge, ios[data.pin].options);

    return data.pin;
}

/**
 * Imports a given pin
 */
app.post('/InitPin', (req, res) => {
    req.on('data', (data) => {
        data = data.toString('ascii');
	    console.log(data);
        try {
            if (isJSON(data)) {
                data = JSON.parse(data);
                initPin(data)
                res.send(ios[data.pin].pin.readSync().toString());
            }
            else {
                res.send('Error: Data was not in JSON format and was expected to be');
            }
        }
        catch(e) {
            let error = {
                message: e.toString(),
                stack: Error().stack
            }
            res.send(JSON.stringify(error));
        }
    })
})

/**
 * Unexports all pins
 */
app.get('/CleanExit', (req, res) => {
    try {
        console.log('Clean Exit');
        let pins = Object.keys(ios);
        for (pin of pins) {
            ios[pin].pin.unexport();
            delete ios[pin];
        }
        res.send('Clean Exit');
    }
    catch(e) {
        let error = {
            message: e.toString(),
            stack: Error().stack
        }
        res.send(JSON.stringify(error));
    }
})

/**
 * Unexports a given pin
 */
app.post('/Unexport', (req, res) => {
    req.on('data', (pin) => {
	pin = pin.toString('ascii');
	console.log(pin);
        try {
            ios[pin].pin.unexport();
            delete ios[pin];
            res.send(`Unexported pin ${pin}`);
        }
        catch(e) {
            let error = {
                message: e.toString(),
                stack: Error().stack
            }
            res.send(JSON.stringify(error));
        }
    })
})

app.post('/Command', (req, res) => {
    req.on('data', (command) => {
        command = command.toString('ascii');
        console.log(command);
        exec(command, (error, stdout, stderr) => {
            if (error) {
                res.send(`Error: ${error.message}`);
            }
            else if (stderr) {
                res.send(`Command Error: ${stderr}`);
            }
            else if (stdout) {
                res.send(stdout);
            }
        })
    })
})

server.on('error', (err) => {
    console.error('Server error:', err);
});

server.listen(port, () => {
    console.log(`PiAPI started on port ${port}`);
});

function isJSON(text) {
    return (/^[\],:{}\s]*$/.test(text.replace(/\\["\\\/bfnrtu]/g, '@').
    replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, ']').
    replace(/(?:^|:|,)(?:\s*\[)+/g, '')))
}
