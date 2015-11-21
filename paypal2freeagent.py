def convert_row(row):
    """
    >>> convert_row(['02/11/2015', '03:06:30', 'GMT', 'Name', 'Type', 'Status', 'GBP', '-7.3', 'Reciept ID', '0.00'])
    ['02/11/2015', '-7.30', 'Name']
    >>> convert_row(['02/11/2015', '03:06:30', 'GMT', 'currency conversion', 'Type', 'Status', 'USD', '-7.3', 'Reciept ID', '0.00'])
    []
    >>> convert_row(['02/11/2015', '03:06:30', 'GMT', 'currency conversion', 'Type', 'Status', 'USD', 'invalid', 'Reciept ID', '0.00'])
    []
    >>> convert_row([])
    Traceback (most recent call last):
     ...
    IndexError: list index out of range
    """
    result = []

    date = row[0]
    description = row[3]
    currency = row[6]
    try:
        amount = '{0:.2f}'.format(float(row[7]))
    except ValueError:
        pass
    else:
        if currency == 'GBP':
            result = [date, amount, description]
    return result

if __name__ == '__main__':
    import csv
    import doctest
    import sys

    tests = doctest.testmod()
    if tests[0]:
        sys.exit(1)

    if len(sys.argv) != 2:
        sys.exit('Please supply a file on which to operate')

    else:
        filtered = []

        with open(sys.argv[1]) as csv_file:
            paypal = csv.reader(csv_file)
            for row in paypal:
                try:
                    row = convert_row(row)
                except IndexError:
                    sys.exit('Failed to convert row - is the format of the file correct?')
                else:
                    if row:
                        filtered.append(row)

        if filtered:
            with open(sys.argv[1], 'w', newline='') as csvfile:
                freeagent = csv.writer(csvfile, csv.QUOTE_MINIMAL)
                for line in filtered:
                    freeagent.writerow(line)
