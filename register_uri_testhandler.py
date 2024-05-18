#!/usr/bin/env python3
import os

# Path to script
executable_path = os.path.expanduser("~/pirate_uri/uri_testhandler.py")

desktop_entry = f"""
[Desktop Entry]
Name=Pirate URI test handler
Exec=gnome-terminal -- python3 {executable_path} %u; echo "Press Enter to exit"; read
Type=Application
MimeType=x-scheme-handler/pirate;
Comment=Test Handler for Pirate URI's
Terminal=false
"""

def register_uri_scheme():
    desktop_path = os.path.expanduser("~/.local/share/applications/pirate-litewallet.desktop")
    with open(desktop_path, 'w') as desktop_file:
        desktop_file.write(desktop_entry)
    print("Desktop entry created. Updating database...")
    os.system("update-desktop-database ~/.local/share/applications")
    print("Update complete. 'pirate:' URI scheme registered.")

if __name__ == "__main__":
    register_uri_scheme()