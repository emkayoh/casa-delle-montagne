#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR" || exit 1

URL="http://127.0.0.1:8000"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/soapbook.log"
PID_FILE="$PROJECT_DIR/.soapbook.pid"

mkdir -p "$LOG_DIR"

# Start Django only if it isn't already available.
if ! /usr/bin/curl -fsS "$URL" >/dev/null 2>&1; then

    if [ ! -f "$PROJECT_DIR/.venv/bin/activate" ]; then
        /usr/bin/osascript -e \
            'display alert "Casa delle Montagne" message "Python virtual environment not found."'
        exit 1
    fi

    source "$PROJECT_DIR/.venv/bin/activate"

    nohup "$PROJECT_DIR/.venv/bin/python" \
        "$PROJECT_DIR/manage.py" \
        runserver 127.0.0.1:8000 --noreload \
        > "$LOG_FILE" 2>&1 &

    echo $! > "$PID_FILE"

    # Wait up to five seconds for Django.
    STARTED=false

    for i in {1..20}; do
        if /usr/bin/curl -fsS "$URL" >/dev/null 2>&1; then
            STARTED=true
            break
        fi

        sleep 0.25
    done

    if [ "$STARTED" != "true" ]; then
        /usr/bin/osascript -e \
            'display alert "Casa delle Montagne" message "The application could not be started. See logs/soapbook.log."'

        exit 1
    fi
fi

/usr/bin/open "$URL"