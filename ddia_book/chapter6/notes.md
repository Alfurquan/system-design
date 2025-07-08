# Partitioning

Partitions are defined in such a way that each piece of data (each record,
row, or document) belongs to exactly one partition. There are various ways of achiev‐
ing this, which we discuss in depth in this chapter. In effect, each partition is a small
database of its own, although the database may support operations that touch multi‐
ple partitions at the same time.

The main reason for wanting to partition data is scalability. Different partitions can
be placed on different nodes in a shared-nothing cluster.

For queries that operate on a single partition, each node can independently execute
the queries for its own partition, so query throughput can be scaled by adding more
nodes. Large, complex queries can potentially be parallelized across many nodes,
although this gets significantly harder.

## Partitioning and Replication

Partitioning is usually combined with replication so that copies of each partition are
stored on multiple nodes. This means that, even though each record belongs to
exactly one partition, it may still be stored on several different nodes for fault toler‐
ance.

A node may store more than one partition. Each
partition’s leader is assigned to one node, and its followers are assigned to other
nodes. Each node may be the leader for some partitions and a follower for other par‐
titions.

## Partitioning of Key-Value Data

Say you have a large amount of data, and you want to partition it. How do you decide
which records to store on which nodes?

Our goal with partitioning is to spread the data and the query load evenly across
nodes. If every node takes a fair share, then—in theory—10 nodes should be able to
handle 10 times as much data and 10 times the read and write throughput of a single
node 

If the partitioning is unfair, so that some partitions have more data or queries than
others, we call it skewed. A partition with disproportion‐
ately high load is called a hot spot.

The simplest approach for avoiding hot spots would be to assign records to nodes
randomly. That would distribute the data quite evenly across the nodes, but it has a
big disadvantage: when you’re trying to read a particular item, you have no way of
knowing which node it is on, so you have to query all nodes in parallel.

### Partitioning by Key Range

One way of partitioning is to assign a continuous range of keys (from some mini‐
mum to some maximum) to each partition. If you know the boundaries between the ranges, you can easily deter‐
mine which partition contains a given key. If you also know which partition is
assigned to which node, then you can make your request directly to the appropriate
node.

**Con**

However, the downside of key range partitioning is that certain access patterns can
lead to hot spots. If the key is a timestamp, then the partitions correspond to ranges
of time—e.g., one partition per day. Unfortunately, because we write data from the
sensors to the database as the measurements happen, all the writes end up going to
the same partition (the one for today), so that partition can be overloaded with writes
while others sit idle

**Solution**

To avoid this problem in the sensor database, you need to use something other than
the timestamp as the first element of the key. For example, you could prefix each
timestamp with the sensor name so that the partitioning is first by sensor name and
then by time. Assuming you have many sensors active at the same time, the write
load will end up more evenly spread across the partitions. Now, when you want to
fetch the values of multiple sensors within a time range, you need to perform a sepa‐
rate range query for each sensor name.

### Partitioning by Hash of Key

Because of this risk of skew and hot spots, many distributed datastores use a hash
function to determine the partition for a given key.

A good hash function takes skewed data and makes it uniformly distributed. Say you
have a 32-bit hash function that takes a string. Whenever you give it a new string, it
returns a seemingly random number between 0 and 2^32 − 1. Even if the input strings
are very similar, their hashes are evenly distributed across that range of numbers.

Once you have a suitable hash function for keys, you can assign each partition a
range of hashes (rather than a range of keys), and every key whose hash falls within a
partition’s range will be stored in that partition.

**Con**

Unfortunately however, by using the hash of the key for partitioning we lose a nice
property of key-range partitioning: the ability to do efficient range queries. Keys that
were once adjacent are now scattered across all the partitions, so their sort order is
lost.

**How Cassandra solves it ?**

A table in Cassandra can be declared with a compound primary key consisting of
several columns. Only the first part of that key is hashed to determine the partition,
but the other columns are used as a concatenated index for sorting the data in Cas‐
sandra’s SSTables. A query therefore cannot search for a range of values within the
first column of a compound key, but if it specifies a fixed value for the first column, it
can perform an efficient range scan over the other columns of the key.

**Practical use case**

The concatenated index approach enables an elegant data model for one-to-many
relationships. For example, on a social media site, one user may post many updates. If
the primary key for updates is chosen to be (user_id, update_timestamp), then you
can efficiently retrieve all updates made by a particular user within some time inter‐
val, sorted by timestamp. Different users may be stored on different partitions, but
within each user, the updates are stored ordered by timestamp on a single partition. 


#### Skewed Workloads and Relieving Hot Spots

Hashing a key to determine its partition can help reduce hot spots.
However, it can’t avoid them entirely: in the extreme case where all reads and writes
are for the same key, you still end up with all requests being routed to the same parti‐
tion.

**Example**

This kind of workload is perhaps unusual, but not unheard of: for example, on a
social media site, a celebrity user with millions of followers may cause a storm of
activity when they do something. This event can result in a large volume of
writes to the same key (where the key is perhaps the user ID of the celebrity, or the ID
of the action that people are commenting on). Hashing the key doesn’t help, as the
hash of two identical IDs is still the same.

**Solution**

Today, most data systems are not able to automatically compensate for such a highly
skewed workload, so it’s the responsibility of the application to reduce the skew. For
example, if one key is known to be very hot, a simple technique is to add a random
number to the beginning or end of the key. Just a two-digit decimal random number
would split the writes to the key evenly across 100 different keys, allowing those keys
to be distributed to different partitions.


## Partitioning and Secondary Indexes

The problem with secondary indexes is that they don’t map neatly to partitions.
There are two main approaches to partitioning a database with secondary indexes:
document-based partitioning and term-based partitioning.

### Partitioning Secondary Indexes by Document

In this indexing approach, each partition is completely separate: each partition main‐
tains its own secondary indexes, covering only the documents in that partition. It
doesn’t care what data is stored in other partitions. Whenever you need to write to
the database—to add, remove, or update a document—you only need to deal with the
partition that contains the document ID that you are writing. For that reason, a
document-partitioned index is also known as a local index.

This approach to querying a partitioned database is sometimes known as scatter/
gather, and it can make read queries on secondary indexes quite expensive. Even if
you query the partitions in parallel, scatter/gather is prone to tail latency amplifica‐
tion.

### Partitioning Secondary Indexes by Term

Rather than each partition having its own secondary index (a local index), we can
construct a global index that covers data in all partitions. However, we can’t just store
that index on one node, since it would likely become a bottleneck and defeat the pur‐
pose of partitioning. A global index must also be partitioned, but it can be partitioned
differently from the primary key index.

The advantage of a global (term-partitioned) index over a document-partitioned
index is that it can make reads more efficient: rather than doing scatter/gather over
all partitions, a client only needs to make a request to the partition containing the
term that it wants. However, the downside of a global index is that writes are slower
and more complicated, because a write to a single document may now affect multiple
partitions of the index (every term in the document might be on a different partition,
on a different node).

## Rebalancing Partitions

The process of moving load from one node in the cluster to another is called reba‐
lancing.

No matter which partitioning scheme is used, rebalancing is usually expected to meet
some minimum requirements:
- After rebalancing, the load (data storage, read and write requests) should be
shared fairly between the nodes in the cluster.
- While rebalancing is happening, the database should continue accepting reads
and writes.
- No more data than necessary should be moved between nodes, to make rebalanc‐
ing fast and to minimize the network and disk I/O load.

### Strategies for Rebalancing

- **How not to do it: hash mod N**

The problem with the mod N approach is that if the number of nodes N changes,
most of the keys will need to be moved from one node to another. For example, say
hash(key) = 123456. If you initially have 10 nodes, that key starts out on node 6
(because 123456 mod 10 = 6). When you grow to 11 nodes, the key needs to move to
node 3 (123456 mod 11 = 3), and when you grow to 12 nodes, it needs to move to
node 0 (123456 mod 12 = 0). Such frequent moves make rebalancing excessively
expensive.

- **Fixed number of partitions**

Fortunately, there is a fairly simple solution: create many more partitions than there
are nodes, and assign several partitions to each node. For example, a database run‐
ning on a cluster of 10 nodes may be split into 1,000 partitions from the outset so that
approximately 100 partitions are assigned to each node.

Now, if a node is added to the cluster, the new node can steal a few partitions from
every existing node until partitions are fairly distributed once again. If a node is removed from the cluster, the same happens in
reverse.

Only entire partitions are moved between nodes. The number of partitions does not
change, nor does the assignment of keys to partitions. The only thing that changes is
the assignment of partitions to nodes. 

- **Dynamic partitioning**

An advantage of dynamic partitioning is that the number of partitions adapts to the
total data volume. If there is only a small amount of data, a small number of parti‐
tions is sufficient, so overheads are small; if there is a huge amount of data, the size of
each individual partition is limited to a configurable maximum.

With dynamic partitioning, the number of partitions is proportional to the size of the
dataset, since the splitting and merging processes keep the size of each partition
between some fixed minimum and maximum. On the other hand, with a fixed num‐
ber of partitions, the size of each partition is proportional to the size of the dataset. In
both of these cases, the number of partitions is independent of the number of nodes.

## Request Routing

We have now partitioned our dataset across multiple nodes running on multiple
machines. But there remains an open question: when a client wants to make a
request, how does it know which node to connect to?

This is an instance of a more general problem called service discovery, which isn’t
limited to just databases. Any piece of software that is accessible over a network has
this problem, especially if it is aiming for high availability (running in a redundant
configuration on multiple machines). 

On a high level, there are a few different approaches to this problem

- Allow clients to contact any node (e.g., via a round-robin load balancer). If that
node coincidentally owns the partition to which the request applies, it can handle
the request directly; otherwise, it forwards the request to the appropriate node,
receives the reply, and passes the reply along to the client.

- Send all requests from clients to a routing tier first, which determines the node
that should handle each request and forwards it accordingly. This routing tier
does not itself handle any requests; it only acts as a partition-aware load balancer.

- Require that clients be aware of the partitioning and the assignment of partitions
to nodes. In this case, a client can connect directly to the appropriate node,
without any intermediary.





