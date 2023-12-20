#!/bin/bash

# Check if the script is run with sudo
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or with sudo."
  exit 1
fi

# Check if the maximum password age is provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <max_password_age>"
  exit 1
fi

# Set the maximum password age
max_password_age="$1"

# Update /etc/login.defs
sed -i "s/^PASS_MAX_DAYS.*/PASS_MAX_DAYS $max_password_age/" /etc/login.defs

# Modify user parameters for all users with a password set
for user in $(awk -F: '$2 != "" {print $1}' /etc/shadow); do
  chage --maxdays "$max_password_age" "$user"
done

echo "Password aging configuration completed successfully."
