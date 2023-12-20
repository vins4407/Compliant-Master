
blockPop3() {
# Check if dovecot-pop3d is installed
POP3D_STATUS=$(dpkg-query -W -f='${db:Status-Status}' dovecot-pop3d 2>/dev/null)

if [ "$POP3D_STATUS" != "installed" ]; then
    echo "dovecot-pop3d is not installed."
    # Additional logic can be added here if needed
else
    echo "Error: dovecot-pop3d is installed. Something went wrong."
    # Additional error-handling logic can be added here if needed
    # For example, attempt to remove the package using: sudo apt purge dovecot-pop3d
fi
}

blockPop3