# Pirate URI Scheme


## Abstract
This document describes the current Pirate Chain URI scheme that is recognized by the current [PirateWallet-lite](https://github.com/PirateNetwork/PirateWallet-Lite) and [Treasure Chest](https://github.com/PirateNetwork/pirate) wallets. 

## Motivation
The purpouse of the URI scheme is to enable users to easily make payments by simply clicking links on webpages or scanning QR codes

## Description
The current Pirate Chain URI scheme is based loosely off the Bitcoin [[1] BIP21](https://github.com/bitcoin/bips/blob/master/bip-0021.mediawiki) proposal with certain modifications. 

* **Note:** *Future iterations are slated to bring the URI handling in line with the Z-cash [[2] ZIP-0321](https://zips.z.cash/zip-0321) proposal. Features of this scheme, such as multiple payment handling, is not yet supported.*

## URI scheme handler
Before a Pirate Chain wallet can respond to URI links, the appropriate URI scheme handler must be registered with the users operating system.

For instructions on registering a URI scheme handler, please refer to the official documentation for the target operating system:

* [Windows: Launch an app with a URI](https://learn.microsoft.com/en-us/windows/uwp/launch-resume/launch-app-with-uri)

* [macOS: URI Scheme Registration](https://developer.apple.com/documentation/bundleresources/information_property_list/cfbundleurltypes)

* [Ubuntu: Gnome Desktop Entry Specification](https://specifications.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html)

**NOTE:** *Specific instructions for registering Pirate Chain wallets will be provided in a later update to this readme*


## General Format
Pirate Chain URIs follow the general format for URIs as set forth in [[3] RFC 3986](https://www.rfc-editor.org/rfc/rfc3986.html). The path component consists of a Pirate Chain address, and the query component provides additional payment options.

Elements of the query component may contain characters outside the valid range. These must first be encoded according to UTF-8, and then each octet of the corresponding UTF-8 sequence must be percent-encoded as described in RFC 3986.


## ABNF grammar

```
 pirateurn     = "pirate:" pirateaddress [ "?" pirateparams ]
 pirateaddress = zs1*( ALPHA / DIGIT )
 pirateparams  = pirateparam [ "&" pirateparams ]
 pirateparam   = [ amountparam / labelparam / messageparam / otherparam / reqparam ]
 amountparam    = "amount=" *digit [ "." *digit ]
 labelparam     = "label=" *qchar
 messageparam   = "message=" *qchar
 otherparam     = qchar *qchar [ "=" *qchar ]
 reqparam       = "req-" qchar *qchar [ "=" *qchar ]
```
Here, "qchar" corresponds to valid characters of an RFC 3986 URI query component, excluding the "=" and "&" characters, which this scheme takes as separators.

The scheme component ("pirate:") is case-insensitive, and implementations must accept any combination of uppercase and lowercase letters. The rest of the URI is case-sensitive, including the query parameter keys.


## Query Keys 


#### address
A valid Pirate Chain [[4] Sapling payment address](https://zips.z.cash/protocol/protocol.pdf#saplingpaymentaddrencoding) string, using [[5] Bech32](https://zips.z.cash/zip-0173)

Sprout addresses are not supported in payment requests as they have been deprecated. Additionally, Transparent addresses are also unsupported in payment requests, as the Pirate Chain network does not permit transparent addresses for peer-to-peer transactions in user wallets.

#### amount 
If an amount is provided, it MUST be specified in decimal ARRR. If a decimal fraction is present then a period (.) MUST be used as the separating character to separate the whole number from the decimal fraction, and both the whole number and the decimal fraction MUST be nonempty. No other separators (such as commas for grouping or thousands) are permitted. Leading zeros in the whole number or trailing zeros in the decimal fraction are ignored. There MUST NOT be more than 8 digits in the decimal fraction.

#### memo
Contents to be included in the Pirate Chain shielded memo field, encoded according to UTF-8, and then each octet of the corresponding UTF-8 sequence must be percent-encoded as described in RFC 3986. The decoded memo contents MUST NOT exceed 512 bytes.

* **Note**: *The memo is encoded per the BIP-021 scheme, which differs from ZIP-0321 where the memo is base64url encoded.*  

#### message
Message that clients can display for the purpose of presenting descriptive information about the payment at the associated paramindex to the user. This message is in wallet only, and not included in the transaction.

* **Note:** *In the Treasure Chest wallet this message is displayed below the memo feild. In the PirateWallet-Lite wallet, the message paramter is not currently displayed*

#### label
Label for an address (e.g. name of receiver). If a label is present at a paramindex, a client rendering a payment for inspection by the user SHOULD display this label (if possible) as well as the associated address. If the label is displayed, it MUST be identifiable as distinct from the address.

* **Note:** *Currently the Treasure Chest and Piratewallet-lite wallets do not display the label paramater*

#### others
Optional, for future extensions. Currently ignored by the wallets

## URI Example Implementation
simple webpage to serve a form that constructs a URI link for testing. Can be accessed at: [Pirate URI Test Page](https://scott-ftf.github.io/pirate_uri/uri.html)

## Examples

Request payment of `1` ARRR

```
pirate:zs178270x3hhlztymvl0q5cht5jfn66ac845rp5gvdvw7prpq4y37qtgq7zhw5l9tf9e5xms5jt8lj?amount=1
```

Request payment amount of `0.1` ARRR, with the memo `Invoice 123` and the message `Thank you for your payment!` 

```
pirate:zs178270x3hhlztymvl0q5cht5jfn66ac845rp5gvdvw7prpq4y37qtgq7zhw5l9tf9e5xms5jt8lj?amount=0.1&memo=invoice%20123&message=Thank%20you%20for%20your%20payment!&label=Test%20Payment
```

---

#### References
[1] [BIP 21: URI Scheme](https://github.com/bitcoin/bips/blob/master/bip-0021.mediawiki)

[2] [ZIP 321: Payment Request URIs](https://zips.z.cash/zip-0321)

[3] [RFC 3986: URI Generic Syntax](https://www.rfc-editor.org/rfc/rfc3986.html)

[4] [Zcash Protocol Specification, Version 2023.4.0. Section 5.6.3.1: Sapling Payment Addresses](https://zips.z.cash/protocol/protocol.pdf#saplingpaymentaddrencoding)

[5] [ZIP 173: Bech32 Format](https://zips.z.cash/zip-0173)


