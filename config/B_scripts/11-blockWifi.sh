

blockWifi() {
# Check if rfkill is available
if command -v rfkill &> /dev/null
then
    # Block all wireless devices
    sudo rfkill block wifi
    echo "WiFi blocked."
else
    echo "rfkill command not found. Please install rfkill."
    sudo apt install rfkill 

fi


}

blockWifi