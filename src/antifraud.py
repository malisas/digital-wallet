#!/usr/bin/python

"""Author: Malisa Smith    Date: 11-08-2016

This program can by run via the following command:
python src/antifraud.py paymo_input/batch_payment.csv paymo_input/stream_payment.csv paymo_output/output1.txt paymo_output/output2.txt paymo_output/output3.txt

It stores all the existing transactions (from batch_payment.csv) in a
dictionary. Then it processes each transactions from
stream_payment.csv, updating the dictionary along the way. For each
new transaction, it prints "unverified" or "trusted" to the
appropriate output file, based on whether the two user Ids involved in
the transaction are in the same network (i.e. > 1, > 2, or > 4 degrees
apart).
"""

import os
import sys

# Returns the degree of distance between id1 and id2 (forwardCurrentIds and backwardCurrentIds).
# Returns 5 for all degrees > 4.
# Searches outwards from both nodes (taking turns) instead of just searching in one direction. This is much faster.
def findDegreeApart(userDict, forwardCurrentIds, forwardPrevIds, backwardCurrentIds, backwardPrevIds, degree):
    if degree == 5:
        # We've reached a base case. return degree
        return degree
    # If the degree is odd, search outwards from the forward-facing nodes
    elif degree % 2 == 1:
        newIds = set()
        for id in forwardCurrentIds:
            neighbors = userDict.get(id, set())
            # Check if the neighbors of the current node intersect
            # With the backwardCurrentIds
            if len(neighbors & backwardCurrentIds) > 0:
                return degree
            else:
                newIds = newIds | neighbors
        # If we reach this point, the forwards and backwards id
        # collections do not intersect for the given degree
        forwardPrevIds = forwardPrevIds | forwardCurrentIds
        # Increment the degrees and repeat the search
        return findDegreeApart(userDict, newIds - forwardPrevIds, forwardPrevIds, backwardCurrentIds, backwardPrevIds, degree + 1)
    # If the degree is even, search outwards from the backwards-facing nodes
    else:
        newIds = set()
        for id in backwardCurrentIds:
            neighbors = userDict.get(id, set())
            # Check if the neighbors of the current node intersect
            # With the forwardCurrentIds
            if len(neighbors & forwardCurrentIds) > 0:
                return degree
            else:
                newIds = newIds | neighbors
        # If we reach this point, the forwards and backwards id
        # Collections do not intersect for the given degree
        backwardPrevIds = backwardPrevIds | backwardCurrentIds
        # Increment the degrees and repeat the search
        return findDegreeApart(userDict, forwardCurrentIds, forwardPrevIds, newIds - backwardPrevIds, backwardPrevIds, degree + 1)

# Records the transaction in the userDict
def storeTransaction(userDict, id1, id2):
    if id1 in userDict:
        userDict[id1].add(id2)
    else:
        userDict[id1] = set([id2])
    # Transaction is recorded once each for id1 and id2
    if id2 in userDict:
        userDict[id2].add(id1)
    else:
        userDict[id2] = set([id1])

# Process the transaction.
# Calls findDegreeApart and storeTransaction
# Also writes trusted/unverified to the appropriate output files
def processTransaction(userDict, id1, id2, output1, output2, output3):
    degreeApart = findDegreeApart(userDict, set([id1]), set(), set([id2]), set(), 1)
    storeTransaction(userDict, id1, id2)

    # If the degree between id1 and id2 is greater than 1, record
    # unverified for Feature 1
    if degreeApart > 1:
        output1.write("unverified\n")
    else:
        output1.write("trusted\n")
    # If the degree between id1 and id2 is greater than 2, record
    # unverified for Feature 2
    if degreeApart > 2:
        output2.write("unverified\n")
    else:
        output2.write("trusted\n")
    # If the degree between id1 and id2 is greater than 4, record
    # unverified for Feature 3
    if degreeApart > 4:
        output3.write("unverified\n")
    else:
        output3.write("trusted\n")

def storeBatchPayments(userDict, batchPayments):
    for line in batchPayments:
        if line.startswith("time,"):
            pass
        # Each transaction line should start with the date. There
        # are some lines which aren't transactions
        elif line.startswith("20"):
            line = line.split(",")
            id1 = line[1].strip(" ")
            id2 = line[2].strip(" ")
            # Record the transaction between the two ids in the
            # user dictionary.
            storeTransaction(userDict, id1, id2)

def processStreamPayments(userDict, streamPayments, output1, output2, output3):
    for line in streamPayments:
        if line.startswith("time,"):
            pass
        elif line.startswith("20"):
            line = line.split(",")
            id1 = line[1].strip(" ")
            id2 = line[2].strip(" ")
            processTransaction(userDict, id1, id2, output1, output2, output3)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    scriptDir = os.path.abspath(__file__)

    # Initialize the dictionary to track all user transactions
    userDict = {}
    # Open up the existing transactions file and record transactions
    with open(os.path.join(os.path.split(os.path.split(scriptDir)[0])[0], argv[1])) as batchPayments:
        storeBatchPayments(userDict, batchPayments)

    # Initialize the 3 output files
    output1 = open(os.path.join(os.path.split(os.path.split(scriptDir)[0])[0], argv[3]), 'w')
    output2 = open(os.path.join(os.path.split(os.path.split(scriptDir)[0])[0], argv[4]), 'w')
    output3 = open(os.path.join(os.path.split(os.path.split(scriptDir)[0])[0], argv[5]), 'w')

    # Now process the new transactions
    with open(os.path.join(os.path.split(os.path.split(scriptDir)[0])[0], argv[2])) as streamPayments:
        processStreamPayments(userDict, streamPayments, output1, output2, output3)

    output1.close()
    output2.close()
    output3.close()

if __name__ == '__main__':
    sys.exit(main())
