   
block_ssh_for_user() {
    local username="$1"
    local sshd_config="/etc/ssh/sshd_config"

    sudo cp "$sshd_config" "${sshd_config}.backup"

    # Remove the user from AllowUsers if present
    sudo sed -i "/AllowUsers.*$username/d" "$sshd_config"

    sudo systemctl restart ssh
    echo "SSH access blocked for user '$username'"
}

main() {
    echo "Block SSH script is running .... "
    echo "asking for Username to remove !! "
    read -p "Enter the username to block SSH access: " username
    echo "got the Username" 
    block_ssh_for_user "$username"
    echo " Done ! You're one more step ahead to harden you system ! "
}

main
