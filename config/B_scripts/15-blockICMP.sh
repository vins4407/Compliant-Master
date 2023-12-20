
blockICMP(){
# Disable acceptance of ICMP redirects
sudo sysctl -w net.ipv4.conf.all.accept_redirects=0
sudo sysctl -w net.ipv4.conf.default.accept_redirects=0

# Disable sending of ICMP redirects
sudo sysctl -w net.ipv4.conf.all.send_redirects=0
sudo sysctl -w net.ipv4.conf.default.send_redirects=0

# If you want to make the changes persistent across reboots, you can edit /etc/sysctl.conf
# and add the following lines:
# net.ipv4.conf.all.accept_redirects = 0
# net.ipv4.conf.default.accept_redirects = 0
# net.ipv4.conf.all.send_redirects = 0
# net.ipv4.conf.default.send_redirects = 0


echo "net.ipv4.conf.all.accept_redirects = 0" >> /etc/sysctl.conf
echo "net.ipv4.conf.default.accept_redirects = 0" >> /etc/sysctl.conf
echo "net.ipv4.conf.all.send_redirects = 0" >> /etc/sysctl.conf
echo "net.ipv4.conf.default.send_redirects = 0" >> /etc/sysctl.conf

sudo sysctl -p

echo "ICMP Redirects have been blocked."

}

blockICMP