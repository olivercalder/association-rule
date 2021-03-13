import itertools as iTools
import association_rule_io as ar_io
import sys
import csv
import json

#input: itemset should be a list of items (each item is a tuple)
#input: transactionset is a list of tuples (tuples represent itemsets)
#input: minsup is an integer representing the minimum support
#method prints out each itemset that meets the support limits and the support associated with that itemset
def apriori(itemset, transactionSet, minsup):

    #L1 is the base case, should hold singular of each item in itemset with support > minsup
    #Filling L1 with all large 1-item sets
    L1 = {}
    for item in itemset:
        count = 0
        for transaction in transactionSet:
            if item in transaction:
                count += 1
        if count >= minsup:
            L1[item] = count

    #AllLarge will hold a list of the large sets
    allLarge = [L1]

    #k represents the LsubKth iteration we are on
    k=2

    #k-2 here because we take one off for the index, and one off because we want to look at the last iteration
    while (len(allLarge[k-2]) !=0):

        #generating and storing candidate sets
        candidateSet = apriori_gen(allLarge[k-2], k)
        candDict = {}
        for cand in candidateSet:
            candDict[cand] = 0

        #calculating which candidates in candidateSet have the adequate support number
        for transaction in transactionSet:
            tnCandSet = subset(candDict, transaction)
            for x in tnCandSet:
                candDict[x] +=1

        #adding candidate sets with appropriate minsup to large itemset list
        Lk = {}
        for key in candDict:
            if candDict[key] >= minsup:
                Lk[key] = candDict[key]
        allLarge.append(Lk)
        k +=1

    #Returning the last non-empty large itemset (with the highest k value)
    # for smallDict in allLarge:
    #     for item in smallDict:
    #         print("Set: " + str(item) + "; Support: " + str(smallDict[item]))

    return allLarge

#function to generate possible candidate sets based on the Lk-1 itemset
#input: largeItemSet should be dict
#input: setLength should be integer
#returns: a list of tuples
def apriori_gen(largeItemSet, setLength):
    #conversion of tuples to set of singular items
    singleSet = set()
    for smallTuple in largeItemSet:
        if(setLength != 2):
            for x in smallTuple:
                singleSet.add(x)
        else:
            singleSet.add(smallTuple)
    #generating all possible combinations of itemset
    return iTools.combinations(list(singleSet), setLength)

#subset function that returns all itemsets that appear in both candidateSet and transaction
#input: candidateSet should be a dictionary of candidates and associated support
#input: transaction should be a list of tuples
#returns: a list of tuples
def subset(candidateSet, transaction):
    outputList = []
    for cand in candidateSet:
        if set(cand).issubset(transaction):
            outputList.append(cand)
    return outputList

#Pre and post processing
def main():
    #Pre-processing
    arg_dict = ar_io.parse_args(sys.argv)
    transactionSet = arg_dict['transactions']
    minsup = arg_dict['min_support']
    itemset = ar_io.get_items(transactionSet)
    sigItemset = apriori(itemset, transactionSet, minsup)

    #Post-processing/formatting outputList
    out_json = arg_dict['out_json']
    outfile = arg_dict['outfile']
    if out_json:
        out_list = []
        for i in range(len(sigItemset)):
            kset = sigItemset[i]
            for singleSet in kset:
                support = kset[singleSet]
                out_list.append([support, singleSet])
        json.dump(out_list, outfile)
    else:
        writer = csv.writer(outfile)
        for i in range(len(sigItemset)):
            kset = sigItemset[i]
            for singleSet in kset:
                support = kset[singleSet]
                writer.writerow([str(support), str(singleSet)])
    if outfile != sys.stdout:
        outfile.close()

if __name__ == '__main__':
    main()
