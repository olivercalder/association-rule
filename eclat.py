import sys
import association_rule_input as ar_input
import time


def get_bit_vectors_and_items(transaction_list):
    full_item_list = []
    for trans_index in range(len(transaction_list)):
        transaction = transaction_list[trans_index]
        for item in transaction:
            full_item_list.append((item, trans_index))

    # Sort the items lexicographically by name
    full_item_list.sort(key=lambda entry: entry[0])

    bit_vectors = []
    # bit_vectors is a list of lists, where each entry is of the form
    # [items, transactions, support], where items is a bit vector encoding
    # which items appear in the itemset, vector is a bit vector encoding which
    # transactions the itemset appears in, and support is the number of
    # transactions in which the itemset occurs.

    items = [full_item_list[0][0]]
    prev_item_name = full_item_list[0][0]
    # Don't want the if-statement to trigger, so initialize to the first item name

    item_bit = 1    # Note: this is the bit itself, not the index of the bit
    transaction_vector = 0
    support = 0
    for (item_name, trans_index) in full_item_list:
        if item_name != prev_item_name:
            # Since full_item_list is sorted, this only occurs once there are
            # no more entries with the previous item name in the list.
            bit_vectors.append((item_bit, transaction_vector, support))
            item_bit <<= 1
            transaction_vector = 0
            support = 0
            items.append(item_name)
            prev_item_name = item_name
        transaction_vector |= (1 << trans_index)
        support += 1

    # Need to add the last item to bit_vectors, since it was not added.
    # Items are only added once the next distinct item is seen.
    bit_vectors.append((item_bit, transaction_vector, support))

    return bit_vectors, items


def get_vector_support(vector):
    support = 0
    while vector:
        support += vector & 1
        vector >>= 1
    return support


def eclat(bit_vectors, min_support):
    # bit_vectors is a list of lists, where each entry is of the form
    # [items, transactions, support], where items is a bit vector encoding
    # which items appear in the itemset, vector is a bit vector encoding which
    # transactions the itemset appears in, and support is the number of
    # transactions in which the itemset occurs.
    # Assumes all items in bit_vectors meet min_support.
    valid_itemset_vectors = []
    for i in range(len(bit_vectors)):
        # This for-loop can be parallelized
        next_vectors = []
        for j in range(i + 1, len(bit_vectors)):
            # This for-loop could also be parallelized, but probably not worth
            # it since the computations are fast and the race conditions for
            # appending to next_vectors could be slow
            item_vector = bit_vectors[i][0] | bit_vectors[j][0]
            transaction_vector = bit_vectors[i][1] & bit_vectors[j][1]
            support = get_vector_support(transaction_vector)
            if support >= min_support:
                next_vectors.append((item_vector, transaction_vector, support))
        if len(next_vectors) > 0:
            valid_itemset_vectors += eclat(next_vectors, min_support)
            valid_itemset_vectors += next_vectors
    return valid_itemset_vectors


def get_itemsets(bit_vectors, items):
    # items is a list of item names, where the index of a given item name
    # corresponds to the bit index of the item in the item bit vectors.
    itemsets = []
    for entry in bit_vectors:
        item_vector = entry[0]
        itemset = []
        for i in range(len(items)):
            if item_vector & (1 << i):
                itemset.append(items[i])
        itemsets.append(itemset)
    return itemsets


def main(transactions, min_support):
    print(f'Creating bit vectors from list of {len(transactions)} transactions... ', end='', file=sys.stderr)
    start_time = time.time()
    initial_bit_vectors, items = get_bit_vectors_and_items(transactions)
    # [initial_]bit_vectors is a list of lists, where each entry is of the form
    # [items, transactions, support], where items is a bit vector encoding
    # which items appear in the itemset, vector is a bit vector encoding which
    # transactions the itemset appears in, and support is the number of
    # transactions in which the itemset occurs.
    end_time = time.time()
    print(end_time - start_time, 'seconds', file=sys.stderr)
    print(f'Found {len(initial_bit_vectors)} distinct items.', file=sys.stderr)

    # items is a list of item names, where the index of a given item name
    # corresponds to the bit index of the item in the item bit vectors.

    print('\nPruning initial (single item) itemsets below MIN_SUP... ', end='', file=sys.stderr)
    start_time = time.time()
    # The eclat() function requires that all items in bit_vectors meet the
    # minimum support, so first prune initial_bit_vectors accordingly.
    bit_vectors = [entry for entry in initial_bit_vectors if entry[2] >= min_support]
    end_time = time.time()
    print(end_time - start_time, 'seconds', file=sys.stderr)
    print(f'Pruned {len(initial_bit_vectors) - len(bit_vectors)} items; {len(bit_vectors)} remain.', file=sys.stderr)

    print('\nRunning the Eclat algorithm on remaining bit vectors... ', end='', file=sys.stderr)
    start_time = time.time()
    # Compute the itemset bit vectors which meet the minimum support
    valid_itemset_vectors = bit_vectors + eclat(bit_vectors, min_support)
    end_time = time.time()
    print(end_time - start_time, 'seconds', file=sys.stderr)
    print(f'Found {len(valid_itemset_vectors)} itemsets which meet minimum support.', file=sys.stderr)

    print('\nSorting itemsets according to support, with greatest support first... ', end='', file=sys.stderr)
    start_time = time.time()
    # OPTIONAL: Sort itemsets so that those with the greatest support appear first
    valid_itemset_vectors.sort(key=lambda entry: entry[2], reverse=True)
    end_time = time.time()
    print(end_time - start_time, 'seconds', file=sys.stderr)
    if len(valid_itemset_vectors) > 0:
        print(f'Itemset with greatest support has support of {valid_itemset_vectors[0][2]}.')

    print('\nBuilding itemset names for valid itemsets... ', end='', file=sys.stderr)
    start_time = time.time()
    # Create a list of itemset names corresponding to valid_itemset_vectors
    itemset_names = get_itemsets(valid_itemset_vectors, items)
    end_time = time.time()
    print(end_time - start_time, 'seconds', file=sys.stderr)

    for i in range(len(valid_itemset_vectors)):
        print(f'Itemset: {itemset_names[i]}\nSupport: {valid_itemset_vectors[i][2]}\n')


if __name__ == '__main__':
    transactions, min_support = ar_input.parse_args(sys.argv)
    main(transactions, min_support)
