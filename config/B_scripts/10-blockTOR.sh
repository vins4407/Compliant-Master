#!/bin/bash

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

        echo "Tor has been disabled."

        }


disable_tor