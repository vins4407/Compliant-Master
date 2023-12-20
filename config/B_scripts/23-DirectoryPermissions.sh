#!/bin/bash

# Check if the script is run with sudo
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or with sudo."
  exit 1
fi

# Check if the desired permissions are provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <desired_permissions_numeric>"
  exit 1
fi

# Get the desired permissions from the first command-line argument
desired_permissions="$1"

# Process each user's home directory
awk -F: '($1 !~ /(halt|sync|shutdown)/ && $7 !~ /^(\/usr)?\/sbin\/nologin(\/)?$/ && $7 !~ /(\/usr)?\/bin\/false(\/)?$/) {print $6}' /etc/passwd | while read -r dir; do
  if [ -d "$dir" ]; then
    dirperm=$(stat -L -c "%a" "$dir")
    if [ "$dirperm" -gt 750 ]; then
      chmod "$desired_permissions" "$dir"
    fi
  fi
done

echo "Permission modification completed successfully."
