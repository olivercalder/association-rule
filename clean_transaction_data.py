import csv
import json

transaction_item_list = []

with open('online_retail.csv') as infile:
    reader = csv.reader(infile)
    for row in reader:
        transaction_id = row[0]
        item_id = row[1]
        if transaction_id != 'InvoiceNo':
            transaction_item_list.append((transaction_id, item_id))

transaction_item_list.sort(key=lambda entry: entry[0])

transactions = []

prev_transaction = transaction_item_list[0][0]
current_items = []
for trans, item in transaction_item_list:
    if trans != prev_transaction:
        transactions.append(tuple(current_items))
        current_items = []
        prev_transaction = trans
    current_items.append(item)
transactions.append(current_items)

with open('transactions.json', 'w') as outfile:
    json.dump(transactions, outfile)
