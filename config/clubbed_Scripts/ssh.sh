#!/bin/bash

# Backup sshd_config
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak

# Disable Password Authentication
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# Disable root login
sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# Allow only specific users (replace "allowed_user" with your username)
#echo "AllowUsers allowed_user" >> /etc/ssh/sshd_config

# Set SSH protocol version to 2
sed -i 's/#Protocol 2/Protocol 2/' /etc/ssh/sshd_config

# Disable empty passwords
sed -i 's/#PermitEmptyPasswords no/PermitEmptyPasswords no/' /etc/ssh/sshd_config

# Disable X11 forwarding
sed -i 's/X11Forwarding yes/X11Forwarding no/' /etc/ssh/sshd_config

# Enable only strong ciphers
echo "Ciphers aes256-ctr,aes192-ctr,aes128-ctr" >> /etc/ssh/sshd_config

# Enable only strong MACs
echo "MACs hmac-sha2-512,hmac-sha2-256" >> /etc/ssh/sshd_config

# Enable only strong key exchange algorithms
echo "KexAlgorithms ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,diffie-hellman-group-exchange-sha256" >> /etc/ssh/sshd_config

# Install and configure Fail2Ban
apt-get update
apt-get install -y fail2ban
systemctl enable fail2ban
systemctl start fail2ban

# Restart SSH service
systemctl restart ssh

echo "Level 2 SSH hardening completed."
