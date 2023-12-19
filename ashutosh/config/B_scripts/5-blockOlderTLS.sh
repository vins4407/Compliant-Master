
# Define vulnerable versions

blockOlderTLS(){

VULNERABLE_VERSIONS=("1.0.1" "1.0.1a" "1.0.1b" "1.0.1c" "1.0.1d" "1.0.1e" "1.0.1f")

# Get OpenSSL version
open_ssl_version=$(openssl version -v | awk '/OpenSSL / {print $2}')

# Check for vulnerability based on version
is_vulnerable=false
for vulnerable_version in "${VULNERABLE_VERSIONS[@]}"; do
  if [[ "$open_ssl_version" == "$vulnerable_version" ]]; then
    is_vulnerable=true
    break
  fi
done

if [[ $is_vulnerable == true ]]; then
  echo "WARNING: OpenSSL version $open_ssl_version is vulnerable to Heartbleed!"

  # Choose update method (comment one out)

  # Option 1: Update system packages (recommended)
  # ----------------------------------------------
  echo "Updating system packages..."
  sudo apt-get update && sudo apt-get upgrade openssl libssl-dev

  # Option 2: Download and install latest version (advanced)
  # ----------------------------------------------
  # echo "Downloading and installing latest OpenSSL..."
  # wget https://www.openssl.org/source/openssl-latest.tar.gz
  # tar xzvf openssl-latest.tar.gz
  # cd openssl-latest
  # ./config && make && sudo make install

  # Replace old symlink with new binary
  sudo ln -sf /usr/local/ssl/bin/openssl `which openssl`

  # Verify update
  echo "Verifying OpenSSL version..."
  openssl version -v

else
  echo "OpenSSL version $open_ssl_version is not vulnerable to Heartbleed."
fi

echo "Patching complete (if vulnerability was present)."


}

blockOlderTLS