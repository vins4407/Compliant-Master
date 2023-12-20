

enableTCP(){
# Check if TCP SYN Cookies are enabled
SYN_COOKIES=$(sysctl -n net.ipv4.tcp_syncookies)

if [ "$SYN_COOKIES" -eq 1 ]; then
    echo "TCP SYN Cookies are already enabled."
else
    # Enable TCP SYN Cookies
    sudo sysctl -w net.ipv4.tcp_syncookies=1

    # If you want to make the change persistent, add the following line to /etc/sysctl.conf:
    echo "net.ipv4.tcp_syncookies = 1" | sudo tee -a /etc/sysctl.conf
    sudo sysctl -p

    echo "TCP SYN Cookies have been enabled."
fi

}
enableTCP