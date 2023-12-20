   
disable_tor(){
        # Stop the Tor service
        result=$(sudo systemctl stop tor)
        if [ $? -eq 0 ]; then
            echo "$result"
        else
            echo "Error disabling Tor: $result"
        fi

        # Disable the Tor service from starting on boot
        result=$(sudo systemctl disable tor)
        if [ $? -eq 0 ]; then
            echo "$result"
        else
            echo "Error disabling Tor: $result"
        fi

        echo "Initial check for blocking tor completed !! " 
        # Block TOR connections using iptables

        sudo iptables -A OUTPUT -p tcp --dport 9001 -j DROP
        sudo iptables -A OUTPUT -p udp --dport 9001 -j DROP
        echo "TOR connections blocked."


        echo "Tor has been disabled."

        }


disable_tor