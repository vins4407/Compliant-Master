setPasswordExpiration(){


    sudo sed -i 's/PASS_MAX_DAYS.*/PASS_MAX_DAYS   90/' /etc/login.defs
    echo "Password expiration set to 90 days."


}



setPasswordExpiration