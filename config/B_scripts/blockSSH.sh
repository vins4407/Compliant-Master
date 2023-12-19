#!/bin/bash

#!/bin/bash

get_allowed_users() {
    sshd_config="/etc/ssh/sshd_config"
    result=$(sudo grep '^AllowUsers' "$sshd_config")

    if [ $? -eq 0 ]; then
        # Extract and return the list of allowed users
        allowed_users=($(echo "$result" | awk '{print $2}'))
        echo "${allowed_users[@]}"
    else
        echo ""
    fi
}

main() {
    allowed_users=($(get_allowed_users))
    total_users=${#allowed_users[@]}

    if [ $total_users -gt 0 ]; then
        echo "SSH is allowed for $total_users user(s):"
        for user in "${allowed_users[@]}"; do
            echo " - $user"
            block_ssh_for_user(user)
        done

        
    else
        echo "SSH is not allowed for any users."
    fi
}

block_ssh_for_user() {
    local username="$1"
    local sshd_config="/etc/ssh/sshd_config"

    sudo cp "$sshd_config" "${sshd_config}.backup"

    # Remove the user from AllowUsers if present
    sudo sed -i "/AllowUsers.*$username/d" "$sshd_config"

    sudo systemctl restart ssh
    echo "SSH access blocked for user '$username'"
}

main



block_ssh_for_user() {
    local username="$1"
    local sshd_config="/etc/ssh/sshd_config"

    sudo cp "$sshd_config" "${sshd_config}.backup"

    # Remove the user from AllowUsers if present
    sudo sed -i "/AllowUsers.*$username/d" "$sshd_config"

    sudo systemctl restart ssh
    echo "SSH access blocked for user '$username'"
}

main
