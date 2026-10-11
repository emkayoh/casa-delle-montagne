#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$PROJECT_DIR/.soapbook.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "Casa delle Montagne is not running."
    exit 0
fi

PID="$(cat "$PID_FILE")"

if kill -0 "$PID" 2>/dev/null; then
    kill "$PID"
    echo "Casa delle Montagne stopped."
else
    echo "Server process was not running."
fi

rm -f "$PID_FILE"