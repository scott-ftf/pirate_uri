import re
from urllib.parse import unquote
import base64
import sys
import termios
import tty


def validate_amount(amount):
    try:
        amount = float(amount)
        if amount > 200000000:
            raise ValueError("Invalid amount. Amount must be less than 200,000,000.")
        # Check if amount has more than 8 decimals
        if len(str(amount).split('.')[1]) > 8:
            raise ValueError("Invalid amount. Amount cannot have more than 8 decimals.")
        return amount
    except ValueError:
        raise ValueError("Invalid amount. Amount must be a decimal number.")


def validate_address(address):
    HRP_REGEX = re.compile("^zs$")
    INVALID_CHAR_REGEX = re.compile("[ib1o]")

    # Trim whitespace from the address
    address = address.strip()

    # Check if a valid address was submitted
    if not address:
        raise ValueError(f"No address included")

    # Get HRP and data parts
    parts = address.split('1')
    hrp, data = parts[0], ''.join(parts[1:])

    # Check that the address starts with zs
    if not HRP_REGEX.match(hrp):
        raise ValueError("Invalid address format. Sapling addresses start with zs1...")

    # Sapling payment addresses must have at least 1 separator
    if '1' not in address:
        raise ValueError("Separator '1' missing. Sapling addresses start with zs1...")

    # Sapling addresses should not have more than one separator (since the HRP does not have a 1)
    if len(parts) != 2:
        raise ValueError("More than one separator '1' found")

    # Check data part does not include characters "i", "b", "1", "o" and uses at least 6 of the allowed characters
    invalid_chars = INVALID_CHAR_REGEX.findall(data)
    if invalid_chars:
        raise ValueError("Invalid data part characters found:", invalid_chars)

    # Check if the address has the correct length (78 characters)
    if len(data) < 75:
        raise ValueError(f"Invalid address length. Sapling addresses have 78 characters ({len(address)} entered)")

    return address


def validate_memo(memo):
    # Check if memo is a valid UTF-8 string with length <= 512 bytes
    try:
        memo_bytes = bytes(memo, 'utf-8')
        if len(memo_bytes) > 512:
            raise ValueError("Invalid memo. Memo cannot exceed 512 bytes.")
    except UnicodeEncodeError:
        raise ValueError("Invalid memo. Memo must be a valid UTF-8 string.")

    # Encode the memo to base64 per Zcash standards
    encoded_memo = base64.b64encode(memo_bytes).decode('utf-8')

    return encoded_memo


def extract_params(uri): 
    # Split the URI into address and query parameters
    prefix, params_str = uri.split('?')

    # Split the prefix into prefix and address
    prefix_parts = prefix.split(':')

    # Check if the prefix matches 'pirate'
    if prefix_parts[0] != "pirate":
        raise ValueError("Invalid URI prefix. Must start with 'pirate:' exactly.")

    # If there's a non-empty address, prepend it to params_str
    if len(prefix_parts) == 2 and prefix_parts[1]:
        params_str = f"address={prefix_parts[1]}&{params_str}"

    # Convert params string to a dictionary
    params_dict = {}
    pairs = params_str.split('&')
    for pair in pairs:
        if '=' in pair:
            key, value = pair.split('=')
            params_dict[key] = value
        else:
            params_dict[pair] = None  # Handle cases like "key" without a value
    return params_dict


def parse_payments(params_dict):
    # Initialize a list to store the dictionaries
    result_list = [{}]

    # Iterate over the keys in the dictionary
    for key, value in params_dict.items():
        # Check if the key has a "." followed by a digit
        if '.' in key:
            key_prefix, index = key.split('.')
            index = int(index)
            # Ensure the list is long enough to accommodate the index
            while len(result_list) < index + 1:
                result_list.append({})
            # Assign the value to the corresponding key in the dictionary at the given index
            result_list[index][key_prefix] = value
        else:
            # Assign the value to the corresponding key in the first dictionary
            result_list[0][key] = value

    return result_list


def validate_payments(payments):
    for payment in payments:
        # Decode URL-encoded values
        for key, value in payment.items():
            payment[key] = unquote(value)

        # Check for duplicate keys within each payment dictionary
        if len(payment) != len(set(payment)):
            raise ValueError("Duplicate keys found in a payment")

        # Check if 'address' key is present
        if 'address' not in payment:
            raise ValueError("Address is missing in a payment")

        # Validate the address
        validate_address(payment['address'])

        # Validate amount if present
        if 'amount' in payment:
            payment['amount'] = validate_amount(payment['amount'])

        # Validate memo if present
        if 'memo' in payment:
            payment['base64_memo'] = validate_memo(payment['memo'])


# TODO: check against ZIP321 rules, BIP21, BIP70, network rules, daemon rules, etc. 
# Only prelimenary checking currently - will need to expand the URI parsing
def parse_uri(uri):    

    try:
        if not uri.startswith("pirate:"):
            raise ValueError("Invalid URI prefix. Must start with 'pirate:'.")
    
        # convert uri to a dict of params
        params = extract_params(uri)

        # Convert from a single mixed dict, to list fo dicts for each payment
        payments = parse_payments(params)
        validate_payments(payments)

        return payments
    except ValueError as e:
        print("Error:", e)


def display_request(payments):
   # Count the number of payments
    num_payments = len(payments)

    # calculate the total payment amount
    total_amount = 0.0
    
    # Get the amount for the current payment
    total_amount = sum(payment.get("amount", 0.0) for payment in payments)

    # Print total payment amount rounded to 5 decimal places
    total_amount_rounded = round(total_amount, 8)
    #print(f"Payment Sum: {total_amount_rounded} ARRR")

    # Print payment fee 
    payment_fee = 0.0001
    #print(f"Payment Fee: {payment_fee} ARRR")

    # Calculate total amount including fee
    total_amount_with_fee = total_amount + payment_fee
    total_amount_with_fee_rounded = round(total_amount_with_fee, 5)
    print(f"Payment Amount: {total_amount_with_fee_rounded} ARRR\n")

    # Print information about the payments
    #print("Payments Addresses:", num_payments)
    for i, payment in enumerate(payments, start=1):
        memo = payment.get("memo")
        if memo:
            print(f"Memo {i}: {memo}")


def process_payment(payments):
        input("\n\nPress any key to exit...")
        sys.exit()


def exit_or_continue():
    print("\nPress Enter to continue, or press Esc to exit: ")
    while True:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        if ch == '\x1b':  # Check for Esc key
            sys.exit()
        elif ch == '\r':  # Check for Enter key
            break
        else:
            print("Invalid input. Please press Enter or Esc.")


def main():
    if len(sys.argv) < 2:
        print("Usage: pirate-uri-handler <URI>")
        sys.exit(1)
    uri = sys.argv[1]    

    # valid testing uri
    #uri = "pirate:zs178270x3hhlztymvl0q5cht5jfn66ac845rp5gvdvw7prpq4y37qtgq7zhw5l9tf9e5xms5jt8lj?amount=0.1&memo=invoice1&message=Thank%20you%20for%20your%20payment!&label=Payment&req=No%20specific%20requirements&other=Additional%20undefined%20information"
    #uri = "pirate:?address=zs178270x3hhlztymvl0q5cht5jfn66ac845rp5gvdvw7prpq4y37qtgq7zhw5l9tf9e5xms5jt8lj&amount=123.456&address.1=zs178270x3hhlztymvl0q5cht5jfn66ac845rp5gvdvw7prpq4y37qtgq7zhw5l9tf9e5xms5jt8lj&amount.1=0.789&memo.1=VGhpcyBpcyBhIHVuaWNvZGUgbWVtbyDinKjwn6aE8J-PhvCfjok"
    #uri = "pirate:?address.0=zs178270x3hhlztymvl0q5cht5jfn66ac845rp5gvdvw7prpq4y37qtgq7zhw5l9tf9e5xms5jt8lj&amount.0=2"

    # invalid testing uri
    #uri = "zcash:zs178270x3hhlztymvl0q5cht5jfn66ac845rp5gvdvw7prpq4y37qtgq7zhw5l9tf9e5xms5jt8lj"
    #uri = "pirate:?amount=1.234&amount=2.345&address=zs178270x3hhlztymvl0q5cht5jfn66ac845rp5gvdvw7prpq4y37qtgq7zhw5l9tf9e5xms5jt8lj"
    #uri = "pirate:?amount=3491405.05201255&address.1=zs178270x3hhlztymvl0q5cht5jfn66ac845rp5gvdvw7prpq4y37qtgq7zhw5l9tf9e5xms5jt8lj&amount.1=5740296.87793245"
    #uri = "pirate:?address=zs178270x3hhlztymvl0q5cht5jfn66ac845rp5gvdvw7prpq4y37qtgq7zhw5l9tf9e5xms5jt8lj&amount=1&amount.1=2&address.2=zs178270x3hhlztymvl0q5cht5jfn66ac845rp5gvdvw7prpq4y37qtgq7zhw5l9tf9e5xms5jt8lj"
    #uri = "pirate://zs178270x3hhlztymvl0q5cht5jfn66ac845rp5gvdvw7prpq4y37qtgq7zhw5l9tf9e5xms5jt8lj?amount=1"

    try:
        payments = parse_uri(uri)
        if payments:
            print("PIRATE PAYMENT REQUEST DETECTED\n")
            display_request(payments)

            print("\n\nOpen Treasure Chest to make this payment") 

            exit_or_continue()
            process_payment(payments)

        else:
            raise ValueError("Payment Request malformed")

    except ValueError as e:
        print("Error:", e)
        input("\n\nPress any key to exit...")
        sys.exit()

if __name__ == "__main__":
    main()