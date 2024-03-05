sudo apt-get update
sudo apt-get upgrade
sudo apt-get autoremove
sudo apt-get autoclean


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
blockIPV6() {

sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1

# If you want to make the changes persistent across reboots, you can edit /etc/sysctl.conf
# and add the following lines:
# net.ipv6.conf.all.disable_ipv6 = 1
# net.ipv6.conf.default.disable_ipv6 = 1

echo "IPv6 has been blocked."

}

blockIPV6