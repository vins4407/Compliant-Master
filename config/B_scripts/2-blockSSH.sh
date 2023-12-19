#!/bin/bash

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

main() {
  while read -r user; do
    block_ssh_for_user "$user"
  done < <(get_allowed_users)

  echo "SSH is not allowed for any users."
}

main
