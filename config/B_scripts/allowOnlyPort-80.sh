

allowOnlyPort80() {

echo ""

iptables -A INPUT -p tcp -m tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT

iptables -A INPUT -I lo -j ACCEPT

iptables -A INPUT -j DROP

}

allowOnlyPort80