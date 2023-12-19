   

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