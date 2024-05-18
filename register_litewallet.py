#!/usr/bin/env python3
import os

# Path to binary
executable_path = os.path.expanduser("~/pirate/piratewallet-lite")

desktop_entry = f"""
[Desktop Entry]
Name=Pirate Lite Wallet
Exec={executable_path} %u
Type=Application
MimeType=x-scheme-handler/pirate;
Comment=Pirate Lite Wallet handles pirate: URIs
Icon=pirate-litewallet-icon
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