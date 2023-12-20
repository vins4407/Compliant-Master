
DisableLoginWithRoot(){

 echo "________________"
 sudo passwd -l root
 echo ""
 echo "Succesfully disabled the root account, meaning you can no longer log in with the root password. "
 echo "" 

 sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
 sudo service ssh restart
 echo "Direct root login disabled."

}

DisableLoginWithRoot