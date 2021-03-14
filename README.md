# association-rule

By Oliver Calder, Theresa Chen, Jaylin Lowe, and Aaron Schondorf, Winter 2021, Carleton College.

## Apriori.py
`Apriori.py` is a simple implementation of the Apriori algorithm.
It takes in a set of items, a set of transactions, and a user-specified minimum support.
It outputs a csv where each row corresponds to a given itemset, with the support value indicating the number of transactions in which the given itemset occurs.
The first column is the support, and all remaining columns are the items in the itemset, so the output is of the form `support,item,item,item,...`.

## eclat.py
`eclat.py` is a simple implementation of the Eclat algorithm, as well as a parallelized implementation which uses the Python `multiprocessing` library to execute the algorithm in parallel using a number of worker processes equal to the number of logical CPU cores on the user's machine.

The input is a list of transactions (identical to that taken by Apriori) and a user-specified minimum support.
It outputs a csv where each row corresponds to a given itemset, with the support value indicating the number of transactions in which the given itemset occurs.
The first column is the support, and all remaining columns are the items in the itemset, so the output is of the form `support,item,item,item,...`.

## Installation and Program Execution

The only external dependency to this program is a functioning Python interpreter, along with the standard libraries with which it usually ships.

Both programs can be invoked using the same command structure:

```
$ python3 Apriori.py [OPTIONS]
$ python3 eclat.py [OPTIONS]
```

The available `OPTIONS` are as follows:

| __Option__            | __Argument__ | __Description__                                                                                       |
| --------              | --------     | --------                                                                                              |
| `-h`, `--help`        |              | Print the usage statement and exit                                                                    |
| `-e`, `--example`     |              | Use the example transaction list, from the Eclat paper (Zaki, 2000).                                  |
| `-c`, `--csv`         | `CSVFILE`    | Read transactions from the given CSV file.                                                            |
| `-C`, `--out-csv`     | `CSVFILE`    | Write output in CSV format to the given file.                                                         |
| `-j`, `--json`        | `JSONFILE`   | Read transactions from the given JSON file.                                                           |
| `-J`, `--out-json`    | `JSONFILE`   | Write output in JSON format to the given file.                                                        |
| `-m`, `--min-support` | `MIN_SUP`    | Sets the minimum support value to `MIN_SUP`.                                                          |
| `-M`, `--min-perc`    | `MIN_PERC`   | Sets the minimum support value to `MIN_PERC`, where `MIN_PERC` is a value between `0.0` and `100.0`.  |
| `-s`, `--stdin`       |              | Read transactions from stdin, assuming one transaction per row in CSV format.                         |
| `-p`, `--parallel`    |              | Use multiple threads to run the algorithm in parallel -- only works for Eclat.                        |

In the case of conflicting arguments, later arguments override earlier arguments.
By default:

- the algorithms use the sample transactions (see below) as though the `-e` argument were passed
- output is written to stdout

Both algorithms also require the shared module `associaiton_rule_io.py`, which is found in this repository as well.

## Sample Datasets

An example data set and transaction set can be found in `association_rule_io.py`, and is as follows:

```
sample_transactions = [
        ('A', 'C', 'T', 'W'),
        ('C', 'D', 'W'),
        ('A', 'C', 'T', 'W'),
        ('A', 'C', 'D', 'W'),
        ('A', 'C', 'D', 'T', 'W'),
        ('C', 'D', 'T')]
```
The algorithms can be run using this sample transaction list by passing the `-e` or `--example` arguments, as described above.

This sample transactions list derives from the list used by Zaki (2000), the paper where the Eclat algorithm was introduced.

Additionally, there are several datafiles derived from the file `online_retail.csv`, which is a dataset of retail transactions available from the [UC Irvine Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Online+Retail).
This dataset has over 4000 items, so running with a low `MIN_SUP` value is *not* recommended.

For the complete dataset, a `MIN_SUP` value of `500` is recommended for a reasonable (sub-5 minute) running time on most machines.
Thus, a recommended run of the algorithms can be invoked as follows:

```
$ python Apriori.py -c transactions-full.csv -C out-apriori.csv -m 500
$ python eclat.py -c transactions-full.csv -C out-eclat.csv -m 500
$ python eclat.py -c transactions-full.csv -C out-eclat-parallel.csv -m 500 -p
```

## Additional Files

There is also two other python programs.

- `clean_transaction_data.py` converts from `online_retail.csv` to `transactions.json`.
- `json2csv.py` converts from a json file (such as `transactions.json`) into a csv file, with the option to include only the first `NUM_ENTRIES` entries -- this can be invoked via `python3 json2csv.py JSONFILE CSVFILE [NUM_ENTRIES]`
