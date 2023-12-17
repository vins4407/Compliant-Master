#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 <script_to_execute.sh>"
    exit 1
fi

script_to_execute="$1"
output_file="output.txt"

# Execute the specified script and redirect both stdout and stderr to the output file
bash "$script_to_execute" >> "$output_file" 2>&1

echo "execution done"

ls 
pwd 