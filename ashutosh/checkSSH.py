import subprocess

def get_allowed_users():
    sshd_config = '/etc/ssh/sshd_config'
    result = subprocess.run(['sudo', 'grep', '^AllowUsers', sshd_config], stdout=subprocess.PIPE)
    
    if result.returncode == 0:
        # Extract and return the list of allowed users
        allowed_users = result.stdout.decode().split()[1:]
        return allowed_users
    else:
        return []

def main():
    allowed_users = get_allowed_users()
    total_users = len(allowed_users)

    if total_users > 0:
        print(f"SSH is allowed for {total_users} user(s):")
        for user in allowed_users:
            print(f" - {user}")
    else:
        print("SSH is not allowed for any users.")

if __name__ == "__main__":
    main()
