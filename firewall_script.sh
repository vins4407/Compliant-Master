
#!/bin/bash

echo ""

# Allow specified ports
IFS=',' read -ra PORTS <<< "80"
for port in "${PORTS[@]}"; do
    iptables -A INPUT -p tcp -m tcp --dport $port -m state --state NEW,ESTABLISHED -j ACCEPT
done

# Allow loopback interface
iptables -A INPUT -i lo -j ACCEPT

# Drop all other incoming traffic
iptables -A INPUT -j DROP
