### Pirate URI Testing Library

This library is only some test files for conversations related to Warelock's [pirate-uri-handler](https://github.com/atlanticFleet/pirate-uri-handler) project

---

#### `uri_test.html` 
simple webpage to serve a uri link for testing. Can be accessed at:
### [Pirate URI Test Page](https://scott-ftf.github.io/pirate_uri/uri_test.html)

note: first register uri's locally with one of the scripts below 

---

#### `register_litewallet.py` 
creates a .desktop entry to register `pirate:` URI links to invoke the lite wallet. Set the path at the top of the script to point to the pirate-litewallet binary

---

#### `register_qt.py`
creates a .desktop entry to register `pirate:` URI links to invoke the Treasure Chest QT wallet. Set the path at the top of the script to point to the pirate-qt-linux binary.

**Note:** QT is not properly handeling URI requests. It responds with "invalid payment address" despite being a proper sapling address. 

Treasure Chest's http paymentserver is running. The `handleURIOrFile` is reacting to the 'pirate:' uri prefix so that higher structure seems to be working and parsing properly in `parseKomodoURI`.

At that point its is validating the `recipient.address` in `IsValidDestinationString` where it is failing to `DecodeDestination`, despite being a valid sapling address. If address calidation is resolved URI parsing should be functional.

Unkown if it has address prefix missmatch from what is defined in the chain params, or something with the checksum. Maybe add debug to trace the data back through the process to see if data is passing correctly, and where exactly it is failing to validate.  

---

#### `register_uri_testhandeler` 
creates a .desktop entry to register `pirate:` URI links to invoke the `url_testhandeler.py` script. Set the path at the top of the script to point to url_testhandeler.py.

This script simply prints the passed data from teh uri link, and provides a entry point do script otehr work to be done n teh URI.

---