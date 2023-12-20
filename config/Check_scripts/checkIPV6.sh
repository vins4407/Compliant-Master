
checkIPV6(){

if ip -6 addr show | grep -q inet6; then
    echo "IPv6 is enabled on this system."
else
    echo "IPv6 is not enabled on this system."
fi

}
checkIPV6