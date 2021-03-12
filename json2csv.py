import sys
import json
import csv

def usage():
    print(f'USAGE: python3 {sys.arv[0]} JSONFILE CSVFILE [ENTRY_NUM]', file=sys.stderr)

def main():
    if len(sys.argv) not in (3, 4):
        print('ERROR: failed to parse arguments', file=sys.stderr)
        usage()
        sys.exit(2)
    json_filename = sys.argv[1]
    csv_filename = sys.argv[2]
    entry_number = None
    if len(sys.argv) == 4:
        entry_number = int(sys.argv[3])

    transactions = []
    with open(json_filename) as infile:
        transactions += json.load(infile)

    if entry_number is None:
        entry_number = len(transactions)

    with open(csv_filename, 'w') as outfile:
        writer = csv.writer(outfile)
        for i in range(min(len(transactions), entry_number)):
            writer.writerow(transactions[i])


if __name__ == '__main__':
    main()
