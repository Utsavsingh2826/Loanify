#!/bin/bash
echo "Checking for processes using port 3000..."

# Find and kill process using port 3000
PID=$(lsof -ti:3000)

if [ -z "$PID" ]; then
    echo "No process is using port 3000"
else
    echo "Found process $PID using port 3000"
    kill -9 $PID
    echo "Process $PID terminated"
    echo "Port 3000 is now free"
fi


