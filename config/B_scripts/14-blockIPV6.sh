
blockIPV6() {

sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1

# If you want to make the changes persistent across reboots, you can edit /etc/sysctl.conf
# and add the following lines:
# net.ipv6.conf.all.disable_ipv6 = 1
# net.ipv6.conf.default.disable_ipv6 = 1

echo "IPv6 has been blocked."

}

blockIPV6