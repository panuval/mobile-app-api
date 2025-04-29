#!/bin/bash

# Script to run python.py in background using nohup

# Set the path to your Python script
PYTHON_SCRIPT="run.py"

# Run the script in the background using nohup
# Output and errors will be saved to nohup.out by default
nohup python "$PYTHON_SCRIPT" &

# Print the process ID so you can track or kill it later if needed
echo "Python script started in background with PID: $!"

# You can also redirect the output to a specific file instead of nohup.out
# nohup python "$PYTHON_SCRIPT" > my_python_output.log 2>&1 &

# Exit successfully
exit 0
