
enableUFW() {
# Check if UFW is installed
if command -v ufw &> /dev/null; then
    echo "UFW is already installed."
else
    # Install UFW
    sudo apt update
    sudo apt install -y ufw

    # Enable UFW
    sudo ufw enable

    echo "UFW has been installed and enabled."
fi
}

enableUFW