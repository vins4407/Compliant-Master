

# THis is LEVEL 2 
hardenIpTables2(){
# Flush existing rules
sudo iptables -F

# Set default policies to DROP
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT

# Allow incoming SSH (Port 22)
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow incoming HTTP (Port 80)
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Allow incoming HTTPS (Port 443)
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow loopback traffic
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A OUTPUT -o lo -j ACCEPT

# Display the rules
sudo iptables -L INPUT -n

}

hardenIpTables2
