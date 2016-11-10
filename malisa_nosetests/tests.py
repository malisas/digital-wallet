import antifraud
from nose.tools import assert_equals
import os
import sys

# sample transactions based on the graph in malisa_test_graph.png
batchPayments = ["2016-11-02 09:38:53, 1, 2, 10, test message",
                 "2016-11-02 09:38:53, 2, 3, 10, test message",
                 "2016-11-02 09:38:53, 3, 4, 10, test message",
                 "2016-11-02 09:38:53, 2, 8, 10, test message",
                 "2016-11-02 09:38:53, 3, 8, 10, test message",
                 "2016-11-02 09:38:53, 4, 6, 10, test message",
                 "2016-11-02 09:38:53, 6, 5, 10, test message",
                 "2016-11-02 09:38:53, 6, 7, 10, test message",
                 "2016-11-02 09:38:53, 7, 10, 10, test message",
                 "2016-11-02 09:38:53, 8, 10, 10, test message",
                 "2016-11-02 09:38:53, 10, 11, 10, test message",
                 "2016-11-02 09:38:53, 11, 12, 10, test message",
                 "2016-11-02 09:38:53, 9, 8, 10, test message",
                 "2016-11-02 09:38:53, 13, 14, 10, test message",
                 "2016-11-02 09:38:53, 14, 15, 10, test message",
                 "2016-11-02 09:38:53, 15, 16, 10, test message",
                 "2016-11-02 09:38:53, 14, 16, 10, test message"]

# sample stream transactions based on the graph in malisa_test_graph_with_streaming.png
streamPayments = ["2016-11-02 09:38:53, 16, 12, 10, test message",
                  "2016-11-02 09:38:53, 16, 12, 10, test message",
                  "2016-11-02 09:38:53, 14, 12, 10, test message",
                  "2016-11-02 09:38:53, 1, 13, 10, test message",
                  "2016-11-02 09:38:53, 1, 14, 10, test message"]

def test_store_transaction():
    userDict = {}
    antifraud.storeTransaction(userDict, "14", "15")
    assert_equals(userDict["15"], set(["14"]))

def test_dictionary_creation():
    userDict = {}
    antifraud.storeBatchPayments(userDict, batchPayments)
    assert_equals(userDict["8"], set(["3", "2", "9", "10"]))
    assert_equals(userDict["1"], set("2"))
    assert_equals(userDict["15"], set(["14", "16"]))

def test_distance_finder():
    userDict = {}
    antifraud.storeBatchPayments(userDict, batchPayments)
    assert_equals(antifraud.findDegreeApart(userDict, set("1"), set(), set("2"), set(), 1), 1)
    assert_equals(antifraud.findDegreeApart(userDict, set("1"), set(), set("3"), set(), 1), 2)
    assert_equals(antifraud.findDegreeApart(userDict, set("1"), set(), set("4"), set(), 1), 3)
    assert_equals(antifraud.findDegreeApart(userDict, set("1"), set(), set("6"), set(), 1), 4)
    assert_equals(antifraud.findDegreeApart(userDict, set("1"), set(), set("5"), set(), 1), 5)
    assert_equals(antifraud.findDegreeApart(userDict, set("1"), set(), set(["10"]), set(), 1), 3)
    assert_equals(antifraud.findDegreeApart(userDict, set("1"), set(), set(["14"]), set(), 1), 5)
    assert_equals(antifraud.findDegreeApart(userDict, set(["16"]), set(), set(["12"]), set(), 1), 5)

def test_single_process_transaction():
    scriptDir = os.path.abspath(__file__)

    # initialize the dictionary to track all user transactions
    userDict = {}
    antifraud.storeBatchPayments(userDict, batchPayments)

    # initialize the 3 output files
    output1 = open(os.path.join(os.path.split(scriptDir)[0], "test_output1.txt"), 'w')
    output2 = open(os.path.join(os.path.split(scriptDir)[0], "test_output2.txt"), 'w')
    output3 = open(os.path.join(os.path.split(scriptDir)[0], "test_output3.txt"), 'w')

    line = streamPayments[0].split(',')
    id1 = line[1].strip(" ")
    id2 = line[2].strip(" ")
    antifraud.processTransaction(userDict, id1, id2, output1, output2, output3)

    output1.close()
    output2.close()
    output3.close()

    expectedOutput1 = "unverified\n"
    expectedOutput2 = "unverified\n"
    expectedOutput3 = "unverified\n"

    output1 = open(os.path.join(os.path.split(scriptDir)[0], "test_output1.txt"), 'r')
    output2 = open(os.path.join(os.path.split(scriptDir)[0], "test_output2.txt"), 'r')
    output3 = open(os.path.join(os.path.split(scriptDir)[0], "test_output3.txt"), 'r')

    assert_equals(output1.read(), expectedOutput1)
    assert_equals(output2.read(), expectedOutput2)
    assert_equals(output3.read(), expectedOutput3)

    output1.close()
    output2.close()
    output3.close()

def test_streaming_transactions():
    scriptDir = os.path.abspath(__file__)

    # initialize the dictionary to track all user transactions
    userDict = {}
    antifraud.storeBatchPayments(userDict, batchPayments)

    # initialize the 3 output files
    output1 = open(os.path.join(os.path.split(scriptDir)[0], "test_output1.txt"), 'w')
    output2 = open(os.path.join(os.path.split(scriptDir)[0], "test_output2.txt"), 'w')
    output3 = open(os.path.join(os.path.split(scriptDir)[0], "test_output3.txt"), 'w')

    antifraud.processStreamPayments(userDict, streamPayments, output1, output2, output3)

    output1.close()
    output2.close()
    output3.close()

    expectedOutput1 = "\n".join(["unverified", "trusted", "unverified", "unverified", "unverified\n"])
    expectedOutput2 = "\n".join(["unverified", "trusted", "trusted", "unverified", "trusted\n"])
    expectedOutput3 = "\n".join(["unverified", "trusted", "trusted", "unverified", "trusted\n"])

    output1 = open(os.path.join(os.path.split(scriptDir)[0], "test_output1.txt"), 'r')
    output2 = open(os.path.join(os.path.split(scriptDir)[0], "test_output2.txt"), 'r')
    output3 = open(os.path.join(os.path.split(scriptDir)[0], "test_output3.txt"), 'r')

    assert_equals(output1.read(), expectedOutput1)
    assert_equals(output2.read(), expectedOutput2)
    assert_equals(output3.read(), expectedOutput3)

    output1.close()
    output2.close()
    output3.close()
