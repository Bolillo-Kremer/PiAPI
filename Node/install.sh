#! /bin/bash

function updatePi() {
    echo "This install requires that you have the latest arm version."
    while true
        do
        read -r -p "Would you like to update your pi? This may take a while [y/n] " input
        
        case $input in
            [yY][eE][sS]|[yY])
        sudo apt-get update
        sudo apt-get upgrade
        break
        ;;
            [nN][oO]|[nN])
        break
        ;;
            *)
        echo "Invalid input..."
        ;;
        esac
        done
}

function installNode() {
    echo Installing Node.js
    updatePi
    newestNodeVersion=$(wget -qO- https://nodejs.org/dist/latest/ | sed -nE 's|.*>node-(.*)\.pkg</a>.*|\1|p')
    sudo wget "https://nodejs.org/dist/latest/node-$newestNodeVersion"-linux-$(uname -m).tar.gz
    echo "Unpacking node-$newestNodeVersion"-linux-$(uname -m).tar.gz
    tar -xzf "node-$newestNodeVersion"-linux-$(uname -m).tar.gz
    cd "node-$newestNodeVersion"-linux-$(uname -m)
    sudo cp -R * /usr/local/
    echo Cleaning up...
    sudo rm "node-$newestNodeVersion"-linux-$(uname -m).tar.gz
    sudo rm -Rf "node-$newestNodeVersion"-linux-$(uname -m)
}

function checkNode() {
    if which node > /dev/null
    then
        echo Node.js already installed
    else
        echo Node.js not installed
        installNode
    fi
}

checkNodeAfterInstall(){
    if which node > /dev/null
    then
        echo Node version $(node -v) installed
        echo Npm version $(npm -v) installed
    else
        echo Node.js install failed. Is $(uname -m) the latest arm version?
        echo Please update your pi and try again or download Node.js manually from nodejs.org
        echo "This PiAPI (Node) may be incompatible with your Pi. Please consider trying PiAPI (Python)."
        while true
            do
            read -r -p "Would you like to try again? [y/n] " input
            
            case $input in
                [yY][eE][sS]|[yY])
                installNode
            break
            ;;
                [nN][oO]|[nN])

            break
            ;;
                *)
            echo "Invalid input..."
            ;;
            esac
            done
    fi
}

function installPiAPI() {
    echo Installing PiAPI
    cd /
    sudo mkdir PiAPI_Node
    cd PiAPI_Node
    sudo wget https://raw.githubusercontent.com/Bolillo-Kremer/PiAPI/master/Node/Server/server.js
    sudo wget https://raw.githubusercontent.com/Bolillo-Kremer/PiAPI/master/Node/Server/package.json
    sudo wget https://raw.githubusercontent.com/Bolillo-Kremer/PiAPI/master/Node/Server/Settings.json
    sudo npm install --save
    echo PiAPI Installed
}

function addToBoot() {
    echo "Adding to boot"
    cd /etc
    sudo sed -i '$ a sudo node /PiAPI_Node/server.js' profile
    sudo sed -i '$ a clear' profile
}

checkNode
installPiAPI
while true
do
 read -r -p "Run PiAPI on boot? [y/n] " input
 
 case $input in
     [yY][eE][sS]|[yY])
 addToBoot
 break
 ;;
    [nN][oO]|[nN])
    break
 ;;
     *)
 echo "Invalid input..."
 ;;
 esac
done

echo "Finished"
