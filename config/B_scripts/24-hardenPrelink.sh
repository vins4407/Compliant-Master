#!/bin/bash

# Check if the script is run with sudo
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or with sudo."
  exit 1
fi

# Verify if prelink is installed
if dpkg -s prelink | grep -qE '(Status:|not installed)'; then
  echo "prelink is not installed."
else
  echo "prelink is installed."

  # Remediation: Restore binaries to normal
  echo "Restoring binaries to normal with prelink -ua"
  prelink -ua

  # Uninstall prelink
  echo "Uninstalling prelink"
  apt purge -y prelink
fi
