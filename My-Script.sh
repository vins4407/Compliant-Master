 
blockBlutooth(){

echo "hardenning Started for Bluetooth"
# Turn off Bluetooth
sudo rmmod --force btusb

echo "The Bluetooth is been Blocked "
echo ""
echo "_______________ Bluetooth Hardenning Successfull !! _________________"

}
blockBlutooth
blockFtpTelnet(){

sudo apt --purge remove xinetd nis yp-tools tftpd atftpd tftpd-hpa telnetd rsh-server rsh-redone-server
sudo apt autoremove 
}

blockFtpTelnet
blockUnusedPackages(){


    sudo apt autoremove 
}

blockUnusedPackages   

blockFailAttemptonSSH(){
# Install Fail2ban
sudo apt install fail2ban

# Backup original jail.conf
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.conf.original

# Configure SSH jail in jail.conf
echo "[sshd]" >> /etc/fail2ban/jail.conf
echo "enabled = true" >> /etc/fail2ban/jail.conf
echo "port = 22" >> /etc/fail2ban/jail.conf
echo "filter = sshd" >> /etc/fail2ban/jail.conf
echo "logpath = /var/log/auth.log" >> /etc/fail2ban/jail.conf
echo "maxretry = 5" >> /etc/fail2ban/jail.conf

# Restart Fail2ban to apply changes
sudo systemctl restart fail2ban

# Verify Fail2ban status
sudo systemctl status fail2ban

echo "Fail2ban installed and configured for SSH. Check the status for confirmation."
}

blockFailAttemptonSSH
# Define vulnerable versions

blockOlderTLS(){

VULNERABLE_VERSIONS=("1.0.1" "1.0.1a" "1.0.1b" "1.0.1c" "1.0.1d" "1.0.1e" "1.0.1f")

# Get OpenSSL version
open_ssl_version=$(openssl version -v | awk '/OpenSSL / {print $2}')

# Check for vulnerability based on version
is_vulnerable=false
for vulnerable_version in "${VULNERABLE_VERSIONS[@]}"; do
  if [[ "$open_ssl_version" == "$vulnerable_version" ]]; then
    is_vulnerable=true
    break
  fi
done

if [[ $is_vulnerable == true ]]; then
  echo "WARNING: OpenSSL version $open_ssl_version is vulnerable to Heartbleed!"

  # Choose update method (comment one out)

  # Option 1: Update system packages (recommended)
  # ----------------------------------------------
  echo "Updating system packages..."
  sudo apt-get update && sudo apt-get upgrade openssl libssl-dev

  # Option 2: Download and install latest version (advanced)
  # ----------------------------------------------
  # echo "Downloading and installing latest OpenSSL..."
  # wget https://www.openssl.org/source/openssl-latest.tar.gz
  # tar xzvf openssl-latest.tar.gz
  # cd openssl-latest
  # ./config && make && sudo make install

  # Replace old symlink with new binary
  sudo ln -sf /usr/local/ssl/bin/openssl `which openssl`

  # Verify update
  echo "Verifying OpenSSL version..."
  openssl version -v

else
  echo "OpenSSL version $open_ssl_version is not vulnerable to Heartbleed."
fi

echo "Patching complete (if vulnerability was present)."


}

blockOlderTLS   
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


get_allowed_users() {
  local sshd_config="/etc/ssh/sshd_config"
  local result=$(sudo grep '^AllowUsers' "$sshd_config") || return 1

  # Extract and return the list of allowed users
  allowed_users=($(echo "$result" | awk '{print $2}'))
  echo "${allowed_users[@]}"
}

block_ssh_for_user() {
  local username="$1"
  local sshd_config="/etc/ssh/sshd_config"

  # Create a backup only once on first call
  [[ ! -f "${sshd_config}.backup" ]] && sudo cp "$sshd_config" "${sshd_config}.backup"

  # Remove the user and restart SSH in one command
  sudo sed -i "/AllowUsers.*$username/d" "$sshd_config" && sudo systemctl restart ssh
  echo "SSH access blocked for user '$username'"
}

blockSSH() {
  while read -r user; do
    block_ssh_for_user "$user"
  done < <(get_allowed_users)

  echo "SSH is not allowed for any users."
}

blockSSH
sudo apt-get update
sudo apt-get upgrade
sudo apt-get autoremove
sudo apt-get autoclean
sudo apt-get install unattended-upgrades -y 
sudo dpkg-reconfigure -plow unattended-upgrades  
blockBlutooth(){

echo "hardenning Started for Bluetooth"
# Turn off Bluetooth
sudo rmmod --force btusb

echo "The Bluetooth is been Blocked "
echo ""
echo "_______________ Bluetooth Hardenning Successfull !! _________________"

}
blockBlutooth
blockFtpTelnet(){

sudo apt --purge remove xinetd nis yp-tools tftpd atftpd tftpd-hpa telnetd rsh-server rsh-redone-server
sudo apt autoremove 
}

blockFtpTelnet
blockUnusedPackages(){


    sudo apt autoremove 
}

blockUnusedPackages   

blockFailAttemptonSSH(){
# Install Fail2ban
sudo apt install fail2ban

# Backup original jail.conf
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.conf.original

# Configure SSH jail in jail.conf
echo "[sshd]" >> /etc/fail2ban/jail.conf
echo "enabled = true" >> /etc/fail2ban/jail.conf
echo "port = 22" >> /etc/fail2ban/jail.conf
echo "filter = sshd" >> /etc/fail2ban/jail.conf
echo "logpath = /var/log/auth.log" >> /etc/fail2ban/jail.conf
echo "maxretry = 5" >> /etc/fail2ban/jail.conf

# Restart Fail2ban to apply changes
sudo systemctl restart fail2ban

# Verify Fail2ban status
sudo systemctl status fail2ban

echo "Fail2ban installed and configured for SSH. Check the status for confirmation."
}

blockFailAttemptonSSH
# Define vulnerable versions

blockOlderTLS(){

VULNERABLE_VERSIONS=("1.0.1" "1.0.1a" "1.0.1b" "1.0.1c" "1.0.1d" "1.0.1e" "1.0.1f")

# Get OpenSSL version
open_ssl_version=$(openssl version -v | awk '/OpenSSL / {print $2}')

# Check for vulnerability based on version
is_vulnerable=false
for vulnerable_version in "${VULNERABLE_VERSIONS[@]}"; do
  if [[ "$open_ssl_version" == "$vulnerable_version" ]]; then
    is_vulnerable=true
    break
  fi
done

if [[ $is_vulnerable == true ]]; then
  echo "WARNING: OpenSSL version $open_ssl_version is vulnerable to Heartbleed!"

  # Choose update method (comment one out)

  # Option 1: Update system packages (recommended)
  # ----------------------------------------------
  echo "Updating system packages..."
  sudo apt-get update && sudo apt-get upgrade openssl libssl-dev

  # Option 2: Download and install latest version (advanced)
  # ----------------------------------------------
  # echo "Downloading and installing latest OpenSSL..."
  # wget https://www.openssl.org/source/openssl-latest.tar.gz
  # tar xzvf openssl-latest.tar.gz
  # cd openssl-latest
  # ./config && make && sudo make install

  # Replace old symlink with new binary
  sudo ln -sf /usr/local/ssl/bin/openssl `which openssl`

  # Verify update
  echo "Verifying OpenSSL version..."
  openssl version -v

else
  echo "OpenSSL version $open_ssl_version is not vulnerable to Heartbleed."
fi

echo "Patching complete (if vulnerability was present)."


}

blockOlderTLS   
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