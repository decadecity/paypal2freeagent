# paypal2freeagent

Convert PayPal CSV export to FreeAgent format.

## Usage:
Download the PayPal transaction history as "Comma Delimited - Balance Affecting Payments".

Run the conversion:
````bash
python3 paypal2freeagent.py [Download.csv]
````
The downloaded file will be converted in place to the [FreeAgent supported format](http://www.freeagent.com/support/kb/banking/file-format-for-bank-upload-csv).

## Caveat user
This will drop all transactions that aren't marked as being in 'GBP'.

