if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or with sudo."
  exit 1
fi

# Function to update pwquality.conf
update_pwquality_conf() {
  local conf_file="/etc/security/pwquality.conf"
  local minlen_option="minlen = $1"
  local minclass_option="minclass = 4"

  # Add or modify minlen option
  if grep -q "^$minlen_option" "$conf_file"; then
    sed -i "s/^minlen =.*/$minlen_option/" "$conf_file"
  else
    echo "$minlen_option" >> "$conf_file"
  fi

  # Add or modify minclass option
  if grep -q "^$minclass_option" "$conf_file"; then
    sed -i "s/^minclass =.*/$minclass_option/" "$conf_file"
  else
    echo "$minclass_option" >> "$conf_file"
  fi
}

# Function to update common-password file
update_common_password() {
  local common_password_file="/etc/pam.d/common-password"
  local pam_pwquality_options="password requisite pam_pwquality.so retry=3"

  # Add pam_pwquality options to common-password file
  if ! grep -q "^$pam_pwquality_options" "$common_password_file"; then
    echo "$pam_pwquality_options" >> "$common_password_file"
  fi
}

# Check if the minimum password length is provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <min_password_length>"
  exit 1
fi

# Set the minimum password length
min_password_length="$1"

# Install pam_pwquality module
apt install -y libpam-pwquality

# Update pwquality.conf
update_pwquality_conf "$min_password_length"

# Update common-password file
update_common_password

echo "Hardening completed successfully."
