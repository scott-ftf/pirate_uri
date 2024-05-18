#!/usr/bin/env python3
import sys
import urllib.parse

def handle_uri(uri):
    parsed = urllib.parse.urlparse(uri)
    if parsed.scheme != 'pirate':
        return False
    print(f"Handling URI: {uri}\n")
    query_params = urllib.parse.parse_qs(parsed.query)
    address = parsed.path.strip('/')
    amount = query_params.get('amount', [None])[0]
    memo = query_params.get('memo', [None])[0]


    # Simulate opening a payment dialog with parsed data
    print(f"Address: {address}")
    print(f"Amount: {amount}")
    print(f"Memo: {memo}")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        uri = sys.argv[1]
        if not handle_uri(uri):
            print("Failed to handle URI.")

    # Wait for user input
    input("Press Enter to exit...")  # Wait for user input before closing