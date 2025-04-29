#!/bin/bash

# Script to shutdown a Python script running in background via nohup

# There are several ways to find and kill the process:

# OPTION 1: If you know the PID (process ID) that was shown when starting the script
# Uncomment and replace PID with the actual process ID
# PID=12345
# if ps -p $PID > /dev/null; then
#     echo "Stopping Python process with PID: $PID"
#     kill $PID
#     echo "Process terminated."
# else
#     echo "Process with PID $PID not found."
# fi

# OPTION 2: Find the process by script name (most common approach)
PYTHON_SCRIPT="run.py"
PIDS=$(pgrep -f "$PYTHON_SCRIPT")

if [ -z "$PIDS" ]; then
    echo "No running processes found for: $PYTHON_SCRIPT"
    exit 1
else
    echo "Found the following processes running $PYTHON_SCRIPT:"
    ps -f -p $PIDS
    
    echo "Terminating processes..."
    for PID in $PIDS; do
        kill $PID
        echo "Sent termination signal to PID: $PID"
    done
    
    # Verify if processes were terminated
    sleep 2
    if pgrep -f "$PYTHON_SCRIPT" > /dev/null; then
        echo "Warning: Some processes did not terminate. Forcing termination..."
        pkill -9 -f "$PYTHON_SCRIPT"
    else
        echo "All processes successfully terminated."
    fi
fi

# Exit successfully
exit 0
