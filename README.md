Malisa Smith's submission to the Insight Data Engineering program

# Running the program

The program is dependent on Python 3.0

Run the command:

```
bash run.sh
```

# Running Nosetests

Run the command:

```
nosetests malisa_nosetests/
```

This will run tests for the following graph:

Batch Payments:

![batch-payments-test](/images/malisa_test_graph.png)

Streaming Payments (alphabetical ordering on edges indicate order of payments):

![streaming-payments-test](/images/malisa_test_graph_with_streaming.png)

GraphViz input (if recreation of graph is desired):

```
graph G {
1 -- 2
2 -- 3
3 -- 4
2 -- 8
3 -- 8
4 -- 6
6 -- 5
6 -- 7
7 -- 10
8 -- 10
10 -- 11
11 -- 12
9 -- 8
13 -- 14
14 -- 15
15 -- 16
14 -- 16
edge[constraint=false]
16 -- 12 [style="dashed" label="a"]
16 -- 12 [style="dashed" label="b"]
14 -- 12 [style="dashed" label="c"]
1 -- 13 [style="dashed" label="d"]
1 -- 14 [style="dashed" label="e"]
}
```
