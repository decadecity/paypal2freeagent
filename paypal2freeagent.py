def convert_paypal_row(row):
    """
    >>> convert_paypal_row(['02/11/2015', '03:06:30', 'GMT', 'Name', 'Type', 'Status', 'GBP', '-7.3', 'Reciept ID', '0.00'])
    ['02/11/2015', '-7.30', 'Name']
    >>> convert_paypal_row(['02/11/2015', '03:06:30', 'GMT', 'currency conversion', 'Type', 'Status', 'USD', '-7.3', 'Reciept ID', '0.00'])
    []
    >>> convert_paypal_row(['02/11/2015', '03:06:30', 'GMT', 'currency conversion', 'Type', 'Status', 'USD', 'invalid', 'Reciept ID', '0.00'])
    []
    >>> convert_paypal_row([])
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

def convert_tide_row(row):
    """
    >>> convert_tide_row(["2017-10-27","2017-10-27 12:35:13","T17102713351310619","DECADE CITY ref: DC HBC","","","1000.00","Faster Payment in",None,"DECADE CITY","DC HBC",None,None,"Cleared"])
    ['27/10/2017', '1000.00', 'DECADE CITY ref: DC HBC']
    >>> convert_tide_row([])
    Traceback (most recent call last):
     ...
    IndexError: list index out of range
    """
    result = []

    try:
        y,m,d = row[0].split('-')
        date = '{}/{}/{}'.format(d,m,y)
    except ValueError:
        return result

    description = row[3]
    try:
        amount = '{0:.2f}'.format(float(row[6]))
        result = [date, amount, description]
    except ValueError:
        pass
    return result

def convertor(row):
    """
    >>> convertor(['02/11/2015', '03:06:30', 'GMT', 'Name', 'Type', 'Status', 'GBP', '-7.3', 'Reciept ID', '0.00']).__name__
    'convert_paypal_row'
    >>> convertor(["2017-10-27","2017-10-27 12:35:13","T17102713351310619","DECADE CITY ref: DC HBC","","","1000.00","Faster Payment in",None,"DECADE CITY","DC HBC",None,None,"Cleared"]).__name__
    'convert_tide_row'
    """
    try:
        amount = '{0:.2f}'.format(float(row[7]))
        return convert_paypal_row
    except ValueError:
        return convert_tide_row

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
            input_data = csv.reader(csv_file)
            for row in input_data:
                convert_row = convertor(row)
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
