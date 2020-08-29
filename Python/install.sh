function installPiAPI() {
    echo Installing PiAPI
    cd /
    sudo mkdir PiAPI_Python
    cd PiAPI_Python
    sudo wget https://raw.githubusercontent.com/Bolillo-Kremer/PiAPI/master/Python/Server/app.py
    sudo wget https://raw.githubusercontent.com/Bolillo-Kremer/PiAPI/master/Python/Server/Settings.json
    pip install flask flask_cors flask_restful
    echo PiAPI Installed
}

function addToBoot() {
    echo "Adding to boot"
    cd /etc
    sudo sed -i '$ a sudo python /PiAPI_Python/app.py' profile
    sudo sed -i '$ a clear' profile
}

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