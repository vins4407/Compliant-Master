
blockImap(){

IMAPD_STATUS=$(dpkg-query -W -f='${db:Status-Status}' dovecot-imapd 2>/dev/null)

if [ "$IMAPD_STATUS" != "installed" ]; then
    echo "dovecot-imapd is not installed."
    # Additional logic can be added here if needed
else
    echo "Error: dovecot-imapd is installed. Something went wrong."
    # Additional error-handling logic can be added here if needed
    # For example, attempt to remove the package using: sudo apt purge dovecot-imapd
fi

}

blockImapPop