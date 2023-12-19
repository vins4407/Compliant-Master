echo "_________ this is goign to block public access ____________ "
sudo mv /etc/resolve.conf /etc/resolve.conf.backup
echo "127.0.0.1 ALL" | sudo tee -a /etc/resolv.conf


echo "_____ DONE -- All website is blocked !  ___________-"