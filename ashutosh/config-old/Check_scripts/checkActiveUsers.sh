   
get_active_users() {
    # Run the 'who' command to get a list of currently logged-in users
    result=$(who 2>&1)

    if [ $? -eq 0 ]; then
        # Parse the output to extract usernames
        active_users=($(echo "$result" | awk '{print $1}'))
        echo "${active_users[@]}"
    else
        echo "Error running 'who' command: $result" >&2
        echo ""
    fi
}

main() {
    active_users=($(get_active_users))
    
    if [ ${#active_users[@]} -gt 0 ]; then
        echo "Currently Active Users:"
        for user in "${active_users[@]}"; do
            echo "$user"
        done
    else
        echo "No active users found."
    fi
}

main
