#!/bin/bash

# Check if the script is run with sudo
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or with sudo."
  exit 1
fi

# Backup the important files
cp /etc/passwd /etc/passwd.bak
cp /etc/shadow /etc/shadow.bak
cp /etc/group /etc/group.bak

# Set secure file permissions
chmod 644 /etc/passwd
chmod 400 /etc/shadow
chmod 644 /etc/group

echo "Backup and secure file permissions set successfully."
