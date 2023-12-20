

blockSNMP() {
    if dpkg-query -W -f='${db:Status-Status}' snmp 2>/dev/null | grep -q installed; then
        echo "SNMP is installed."

        sudo apt purge snmp -y 
        echo "snmp has been removed."
        
    else
        echo "SNMP  is not installed."
    fi
}

blockSNMP
