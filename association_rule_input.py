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

    -j  --json JSONFILE: read transactions from the given JSON file

    -m  --min-support INT: set the minimum support value to INT

    -M  --min-perc FLOAT: set the minimum support percentage to FLOAT, where
                FLOAT is a value between 0.0 and 100.0

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
        optlist, args = getopt.gnu_getopt(args, 'hepc:j:m:M:s:', ['help', 'example', 'parallel', 'csv=', 'json=', 'min-sup=', 'min-perc=', 'stdin'])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    transactions = sample_transactions
    min_support = 3
    min_percent = 0.0
    for o, a in optlist:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-e', '--example'):
            transactions = sample_transactions
        elif o in ('-p', '--parallel'):
            # Use threading to do parallelization, maybe
            pass
        elif o in ('-c', '--csv'):
            transactions = parse_transactions_from_csv(a)
        elif o in ('-j', '--json'):
            transactions = parse_transactions_from_json(a)
        elif o in ('-m', '--min-sup'):
            min_support = int(a)
        elif o in ('-M', '--min-perc'):
            min_percent = float(a)
        elif o in ('-s', '--stdin'):
            transactions = parse_transactions_from_stdin()
        else:
            assert False, f'Unknown option: {o}'
    if min_percent:
        min_support = int(min_percent * len(transactions))
    return (transactions, min_support)


