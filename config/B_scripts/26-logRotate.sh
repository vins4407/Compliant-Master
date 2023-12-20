#!/bin/bash

# Check if the script is run with sudo
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or with sudo."
  exit 1
fi

# Backup original logrotate configuration
cp /etc/logrotate.conf /etc/logrotate.conf.backup

# Configure logrotate for enhanced log management
cat <<EOF > /etc/logrotate.conf
weekly
rotate 4
create
dateext
dateformat -%Y-%m-%d
compress
delaycompress
missingok
notifempty
ifempty
sharedscripts
postrotate
    systemctl restart rsyslog
endscript
EOF

echo "Logrotate configured for enhanced log management."
