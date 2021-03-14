import getopt
import json
import csv
import sys


def usage():
    print(f'''USAGE: python3 {sys.argv[0]} OPTIONS

OPTIONS:

    -h  --help: print this usage statement and exit

    -e  --example: use example transactions from the Eclat paper

    -c  --csv CSVFILE: read transactions from the given CSV file

    -C  --out-csv CSVFILE: write output in CSV format to the given file

    -j  --json JSONFILE: read transactions from the given JSON file

    -J  --out-json JSONFILE: write output in JSON format to the given file

    -m  --min-support MIN_SUP: set the minimum support value to MIN_SUP

    -M  --min-perc MIN_PERC: set the minimum support percentage to MIN_PERC,
                where MIN_PERC is a value between 0.0 and 100.0

    -s  --stdin: read transactions from stdin, assuming one transaction per
                row in CSV format

    -p  --parallel: use multiple threads to run the algorithm in parallel, if
                the algorithm supports parallel processing
''', file=sys.stderr)


sample_transactions = [
        ('A', 'C', 'T', 'W'),
        ('C', 'D', 'W'),
        ('A', 'C', 'T', 'W'),
        ('A', 'C', 'D', 'W'),
        ('A', 'C', 'D', 'T', 'W'),
        ('C', 'D', 'T')]


def get_items(transactions):
    complete_item_list = []
    for transaction in transactions:
        complete_item_list += transaction
    complete_item_list.sort()
    unique_items = []
    curr_item = ''
    for item in complete_item_list:
        if item != curr_item:
            unique_items.append(item)
            curr_item = item
    return unique_items


def parse_transactions_from_csv(filename):
    transactions = []
    with open(filename) as infile:
        reader = csv.reader(infile)
        for row in reader:
            transactions.append(tuple([item for item in row if item]))
    return transactions


def parse_transactions_from_json(filename):
    transactions = []
    with open(filename) as infile:
        json_transactions = json.load(infile)
        for transaction in json_transactions:
            transactions.append(tuple(transaction))
    return transactions


def parse_transactions_from_stdin():
    transactions = []
    reader = csv.reader(sys.stdin)
    for row in reader:
        transactions.append(tuple([item for item in row if item]))
    return transactions


def parse_args(args):
    try:
        optlist, args = getopt.gnu_getopt(args, 'hepc:C:j:J:m:M:s:', ['help', 'example', 'parallel', 'csv=', 'csv-out=', 'json=', 'json-out=', 'min-sup=', 'min-perc=', 'stdin'])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    arg_dict = {
            'transactions' : sample_transactions,
            'min_support'  : 3,
            'outfile'      : sys.stdout,
            'out_json'     : False
            }
    min_percent = 0.0
    out_filename = ''
    out_json = False
    for o, a in optlist:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-e', '--example'):
            arg_dict['transactions'] = sample_transactions
        elif o in ('-p', '--parallel'):
            # Use threading to do parallelization, if algorithm supports it
            arg_dict['parallel'] = True
        elif o in ('-c', '--csv'):
            arg_dict['transactions'] = parse_transactions_from_csv(a)
        elif o in ('-C', '--csv-out'):
            out_filename = a
            out_json = False
        elif o in ('-j', '--json'):
            transactions = parse_transactions_from_json(a)
        elif o in ('-J', '--json-out'):
            out_filename = a
            out_json = True
        elif o in ('-m', '--min-sup'):
            arg_dict['min_support'] = int(a)
        elif o in ('-M', '--min-perc'):
            min_percent = float(a)
        elif o in ('-s', '--stdin'):
            transactions = parse_transactions_from_stdin()
        else:
            assert False, f'Unknown option: {o}'
    if min_percent:
        arg_dict['min_support'] = int(min_percent * 0.01 * len(transactions))
    if out_filename:
        arg_dict['outfile'] = open(out_filename, 'w')
    else:
        arg_dict['out_json'] = False
    return arg_dict
