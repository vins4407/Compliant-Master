blockUsb(){


echo "USB is command is runnig"

sleep 5 

sudo echo "blacklist usb-storage" >> /etc/modprobe.d/blacklist.conf
 
echo "Execution  COmpleted for USB blocking"

}

blockUsb