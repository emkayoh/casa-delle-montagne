# Casa delle Montagne — macOS Application Launcher

**Document version:** 1.0  
**Date:** 11 October 2026  
**Status:** Working procedure  
**Purpose:** Create a clickable macOS application that starts the local Django application and opens it in the default web browser.

---

## 1. Overview

The Casa delle Montagne application is a Django web application intended to run locally.

For normal use on macOS, the user should not need to open Terminal, activate a Python environment, or run Django manually. A small macOS `.app` launcher is therefore created which:

1. checks whether the local Django application is already running;
2. starts it if necessary;
3. opens the application in the default browser.

The resulting application can be placed on the Desktop or in the Applications folder and launched by double-clicking its icon.

---

## 2. Assumed project structure

This procedure assumes a project structure broadly like:

```text
soapbook/
├── .venv/
├── inventory/
├── soapbook/
├── manage.py
├── requirements.txt
└── run_app.sh
```

The project contains the Casa delle Montagne branding image at:

```text
inventory/static/inventory/images/brand.png
```

The exact project location will vary between machines.

Examples in this document use:

```text
/Users/USERNAME/Code/soapbook
```

Replace this with the actual path returned by:

```bash
pwd
```

---

## 3. Create the launcher script

From the root of the Django project, create:

```bash
touch run_app.sh
chmod +x run_app.sh
```

Add:

```bash
#!/bin/bash

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

URL="http://127.0.0.1:8000"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/soapbook.log"
PID_FILE="$PROJECT_DIR/.soapbook.pid"

mkdir -p "$LOG_DIR"

# Start Django only if it is not already responding.
if ! /usr/bin/curl -fsS "$URL" >/dev/null 2>&1; then

    source "$PROJECT_DIR/.venv/bin/activate"

    nohup python manage.py runserver 127.0.0.1:8000 \
        > "$LOG_FILE" 2>&1 &

    echo $! > "$PID_FILE"

    # Allow Django time to start before opening the browser.
    for i in {1..20}; do
        if /usr/bin/curl -fsS "$URL" >/dev/null 2>&1; then
            break
        fi
        sleep 0.25
    done
fi

/usr/bin/open "$URL"
```

### Runtime files

Add the following to `.gitignore`:

```text
logs/
.soapbook.pid
```

These files are generated locally and should not be committed.

---

## 4. Test the shell launcher

Before creating the macOS application wrapper, test the launcher directly:

```bash
./run_app.sh
```

Expected behaviour:

```text
run_app.sh
    ↓
Is http://127.0.0.1:8000 responding?
    ├── yes → open browser
    └── no  → activate virtual environment
              start Django
              wait for server
              open browser
```

Running the script a second time should not start a second Django server. It should simply open the application again in the browser.

If the application does not start, inspect:

```text
logs/soapbook.log
```

---

## 5. Create the AppleScript wrapper

Create a file named:

```text
launcher.applescript
```

containing:

```applescript
do shell script "/bin/bash '/Users/USERNAME/Code/soapbook/run_app.sh'"
```

Replace the example path with the absolute path to the project.

For example, obtain the project path with:

```bash
pwd
```

---

## 6. Compile the macOS application

Compile the AppleScript into a macOS `.app` bundle:

```bash
osacompile \
    -o "$HOME/Desktop/Casa delle Montagne.app" \
    launcher.applescript
```

This creates:

```text
~/Desktop/Casa delle Montagne.app
```

Double-click the application to test it.

Expected behaviour:

1. no Terminal window remains open;
2. Django starts if necessary;
3. the default browser opens;
4. the Casa delle Montagne product page is displayed.

---

## 7. Application icon

### 7.1 Attempted bundle icon method

A conventional macOS `.icns` file can be generated from the square branding image using `sips` and `iconutil`.

For reference:

```bash
mkdir -p Casa.iconset

sips -z 16 16     inventory/static/inventory/images/brand.png --out Casa.iconset/icon_16x16.png
sips -z 32 32     inventory/static/inventory/images/brand.png --out Casa.iconset/icon_16x16@2x.png

sips -z 32 32     inventory/static/inventory/images/brand.png --out Casa.iconset/icon_32x32.png
sips -z 64 64     inventory/static/inventory/images/brand.png --out Casa.iconset/icon_32x32@2x.png

sips -z 128 128   inventory/static/inventory/images/brand.png --out Casa.iconset/icon_128x128.png
sips -z 256 256   inventory/static/inventory/images/brand.png --out Casa.iconset/icon_128x128@2x.png

sips -z 256 256   inventory/static/inventory/images/brand.png --out Casa.iconset/icon_256x256.png
sips -z 512 512   inventory/static/inventory/images/brand.png --out Casa.iconset/icon_256x256@2x.png

sips -z 512 512   inventory/static/inventory/images/brand.png --out Casa.iconset/icon_512x512.png
sips -z 1024 1024 inventory/static/inventory/images/brand.png --out Casa.iconset/icon_512x512@2x.png

iconutil -c icns Casa.iconset -o Casa.icns
```

In testing, however, the compiled AppleScript application continued to display the standard AppleScript scroll icon despite changing the bundle icon metadata.

### 7.2 Working method

The reliable method was to assign the artwork as a Finder custom icon.

1. Open `brand.png` in **Preview**.
2. Press `Cmd-A`.
3. Press `Cmd-C`.
4. In Finder, select **Casa delle Montagne.app**.
5. Press `Cmd-I` to open **Get Info**.
6. Click the small application icon at the top-left of the Get Info window.
7. Press `Cmd-V`.

The Casa delle Montagne artwork should immediately become the application icon.

This method worked correctly in both Desktop and Finder views.

---

## 8. Files that should be version controlled

The following should normally be committed:

```text
run_app.sh
launcher.applescript
inventory/static/inventory/images/brand.png
docs/macos_launcher.md
```

The compiled application itself does not need to be version controlled unless there is a specific reason to distribute it through Git.

Generated or machine-specific files should normally remain untracked:

```text
logs/
.soapbook.pid
Casa.iconset/
Casa.icns
Casa delle Montagne.app
```

Suggested `.gitignore` additions:

```text
logs/
.soapbook.pid
Casa.iconset/
Casa.icns
*.app/
```

---

## 9. Rebuilding the launcher on another Mac

On another macOS machine:

1. clone or copy the repository;
2. create the Python virtual environment;
3. install the dependencies;
4. run the Django migrations;
5. test `run_app.sh`;
6. edit `launcher.applescript` so that it contains the correct absolute project path;
7. compile the `.app` with `osacompile`;
8. apply the custom icon through Finder → Get Info.

The launcher is therefore easy to reconstruct without storing the compiled `.app` in Git.

---

## 10. Current limitations

This launcher uses Django's development server:

```bash
python manage.py runserver
```

This is acceptable for the present local prototype.

For a permanent installation, particularly on the Ubuntu machine intended for the soapmaker, the preferred arrangement is likely to be:

```text
user login
    ↓
systemd user service starts application
    ↓
desktop launcher opens browser
```

In that arrangement the desktop icon would no longer be responsible for starting Django; it would simply open the already-running local application.

---

## 11. Version history

| Version | Date | Change |
|---|---|---|
| 1.0 | 11 October 2026 | Initial documented macOS launcher procedure. Includes working shell launcher, AppleScript application wrapper, and Finder custom-icon method. |
