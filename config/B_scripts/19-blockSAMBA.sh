

blockSAMBA(){
if dpkg-query -W -f='${db:Status-Status}' samba 2>/dev/null | grep -q installed; then
    echo "Samba is installed."

    sudo apt purge samba -y
    echo "Samba has been removed."
   
else
    echo "Samba is not installed."
fi


}

blockSAMBA