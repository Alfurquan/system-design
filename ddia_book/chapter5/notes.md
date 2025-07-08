# Shared nothing Architecture

Shared-nothing architectures (sometimes called horizontal scaling or
scaling out) have gained a lot of popularity. In this approach, each machine or virtual
machine running the database software is called a node. Each node uses its CPUs,
RAM, and disks independently. Any coordination between nodes is done at the soft‐
ware level, using a conventional network.

# Replication vs partitioning

There are two common ways data is distributed across multiple nodes:

- **Replication**
Keeping a copy of the same data on several different nodes, potentially in differ‐
ent locations. Replication provides redundancy: if some nodes are unavailable,
the data can still be served from the remaining nodes. Replication can also help
improve performance.

- **Partitioning**
Splitting a big database into smaller subsets called partitions so that different par‐
titions can be assigned to different nodes (also known as sharding).

# Replication

There are several reasons why you might want to replicate data:
- To keep data geographically close to your users (and thus reduce latency)
- To allow the system to continue working even if some of its parts have failed
(and thus increase availability)
- To scale out the number of machines that can serve read queries (and thus
increase read throughput)

## Leaders and followers

Each node that stores a copy of the database is called a replica. With multiple replicas,
a question inevitably arises: how do we ensure that all the data ends up on all the rep‐
licas?

Every write to the database needs to be processed by every replica; otherwise, the rep‐
licas would no longer contain the same data. The most common solution for this is
called leader-based replication. It works as follows:

- One of the replicas is designated the leader (also known as master or primary).
When clients want to write to the database, they must send their requests to the
leader, which first writes the new data to its local storage.

- The other replicas are known as followers (read replicas, slaves, secondaries, or hot
standbys) Whenever the leader writes new data to its local storage, it also sends
the data change to all of its followers as part of a replication log or change stream.
Each follower takes the log from the leader and updates its local copy of the data‐
base accordingly, by applying all writes in the same order as they were processed
on the leader.

- When a client wants to read from the database, it can query either the leader or
any of the followers. However, writes are only accepted on the leader

Leader-based replication is not restricted to only databases: distributed message brokers such as Kafka and
RabbitMQ highly available queues also use it. 

## Synchronous Versus Asynchronous Replication

An important detail of a replicated system is whether the replication happens syn‐
chronously or asynchronously.

The advantage of synchronous replication is that the follower is guaranteed to have
an up-to-date copy of the data that is consistent with the leader. If the leader sud‐
denly fails, we can be sure that the data is still available on the follower. The disad‐
vantage is that if the synchronous follower doesn’t respond (because it has crashed,
or there is a network fault, or for any other reason), the write cannot be processed.
The leader must block all writes and wait until the synchronous replica is available
again.

For that reason, it is impractical for all followers to be synchronous: any one node
outage would cause the whole system to grind to a halt. In practice, if you enable syn‐
chronous replication on a database, it usually means that one of the followers is syn‐
chronous, and the others are asynchronous. If the synchronous follower becomes
unavailable or slow, one of the asynchronous followers is made synchronous. This
guarantees that you have an up-to-date copy of the data on at least two nodes: the
leader and one synchronous follower. This configuration is sometimes also called
semi-synchronous.

Often, leader-based replication is configured to be completely asynchronous. In this
case, if the leader fails and is not recoverable, any writes that have not yet been repli‐
cated to followers are lost. This means that a write is not guaranteed to be durable,
even if it has been confirmed to the client. However, a fully asynchronous configura‐
tion has the advantage that the leader can continue processing writes, even if all of its
followers have fallen behind.

## Setting up new followers

- Take a consistent snapshot of the leader’s database at some point in time—if pos‐
sible, without taking a lock on the entire database. Most databases have this fea‐
ture, as it is also required for backups. In some cases, third-party tools are
needed, such as innobackupex for MySQL.
- Copy the snapshot to the new follower node.
- The follower connects to the leader and requests all the data changes that have
happened since the snapshot was taken. This requires that the snapshot is associ‐
ated with an exact position in the leader’s replication log. That position has vari‐
ous names: for example, PostgreSQL calls it the log sequence number, and
MySQL calls it the binlog coordinates.
- When the follower has processed the backlog of data changes since the snapshot,
we say it has caught up. It can now continue to process data changes from the
leader as they happen.

## Handling node outages

Any node in the system can go down, perhaps unexpectedly due to a fault, but just as
likely due to planned maintenance (for example, rebooting a machine to install a ker‐
nel security patch). Thus, our goal is to keep the system as a
whole running despite individual node failures, and to keep the impact of a node out‐
age as small as possible.

### Follower failure: Catch-up recovery

On its local disk, each follower keeps a log of the data changes it has received from
the leader. If a follower crashes and is restarted, or if the network between the leader
and the follower is temporarily interrupted, the follower can recover quite easily:
from its log, it knows the last transaction that was processed before the fault occur‐
red. Thus, the follower can connect to the leader and request all the data changes that
occurred during the time when the follower was disconnected. When it has applied
these changes, it has caught up to the leader and can continue receiving a stream of
data changes as before.

### Leader failure: Failover

Handling a failure of the leader is trickier: one of the followers needs to be promoted
to be the new leader, clients need to be reconfigured to send their writes to the new
leader, and the other followers need to start consuming data changes from the new
leader. This process is called failover.

An automatic failover process usually consists of the following steps:

- Determining that the leader has failed.
- Choosing a new leader: The best candidate for
leadership is usually the replica with the most up-to-date data changes from the
old leader (to minimize any data loss). Getting all the nodes to agree on a new
leader is a consensus problem.
- Reconfiguring the system to use the new leader. 

## Implementation of Replication Logs

### Write-ahead log (WAL) shipping

The log is an append-only sequence of bytes containing all writes to the
database. We can use the exact same log to build a replica on another node: besides
writing the log to disk, the leader also sends it across the network to its followers.
When the follower processes this log, it builds a copy of the exact same data struc‐
tures as found on the leader.

### Logical (row-based) log replication

A logical log for a relational database is usually a sequence of records describing
writes to database tables at the granularity of a row:
- For an inserted row, the log contains the new values of all columns.
- For a deleted row, the log contains enough information to uniquely identify the
row that was deleted. Typically this would be the primary key, but if there is no
primary key on the table, the old values of all columns need to be logged.
- For an updated row, the log contains enough information to uniquely identify
the updated row, and the new values of all columns (or at least the new values of
all columns that changed)

A transaction that modifies several rows generates several such log records, followed
by a record indicating that the transaction was committed

## Problems with Replication Lag

Leader-based replication requires all writes to go through a single node, but readonly queries can go to any replica. For workloads that consist of mostly reads and only a small percentage of writes (a common pattern on the web), there is an attrac‐
tive option: create many followers, and distribute the read requests across those fol‐
lowers. This removes load from the leader and allows read requests to be served by
nearby replicas.

Unfortunately, if an application reads from an asynchronous follower, it may see out‐
dated information if the follower has fallen behind. This leads to apparent inconsis‐
tencies in the database: if you run the same query on the leader and a follower at the
same time, you may get different results, because not all writes have been reflected in
the follower. This inconsistency is just a temporary state—if you stop writing to the
database and wait a while, the followers will eventually catch up and become consis‐
tent with the leader. For that reason, this effect is known as eventual consistency.

### Reading Your Own Writes

Many applications let the user submit some data and then view what they have sub‐
mitted. This might be a record in a customer database, or a comment on a discussion
thread, or something else of that sort. When new data is submitted, it must be sent to
the leader, but when the user views the data, it can be read from a follower. This is
especially appropriate if data is frequently viewed but only occasionally written.

With asynchronous replication, there is a problem, if the
user views the data shortly after making a write, the new data may not yet have
reached the replica. To the user, it looks as though the data they submitted was lost,
so they will be understandably unhappy.
In this situation, we need read-after-write consistency, also known as read-your-writes
consistency

**How can we implement read-after-write consistency in a system with leader-based
replication?**

- When reading something that the user may have modified, read it from the
leader; otherwise, read it from a follower. This requires that you have some way
of knowing whether something might have been modified, without actually
querying it. For example, user profile information on a social network is nor‐
mally only editable by the owner of the profile, not by anybody else. Thus, a sim‐
ple rule is: always read the user’s own profile from the leader, and any other
users’ profiles from a follower.

- If most things in the application are potentially editable by the user, that
approach won’t be effective, as most things would have to be read from the
leader (negating the benefit of read scaling). In that case, other criteria may be
used to decide whether to read from the leader. For example, you could track the
time of the last update and, for one minute after the last update, make all reads
from the leader.

- The client can remember the timestamp of its most recent write—then the sys‐
tem can ensure that the replica serving any reads for that user reflects updates at
least until that timestamp. If a replica is not sufficiently up to date, either the read
can be handled by another replica or the query can wait until the replica has
caught up. The timestamp could be a logical timestamp (something that indicates
ordering of writes, such as the log sequence number) or the actual system clock
(in which case clock synchronization becomes critical).

Another complication arises when the same user is accessing your service from mul‐
tiple devices, for example a desktop web browser and a mobile app. In this case you
may want to provide cross-device read-after-write consistency: if the user enters some
information on one device and then views it on another device, they should see the
information they just entered.

In this case, there are some additional issues to consider:
- Approaches that require remembering the timestamp of the user’s last update
become more difficult, because the code running on one device doesn’t know
what updates have happened on the other device. This metadata will need to be
centralized.
- If your replicas are distributed across different datacenters, there is no guarantee
that connections from different devices will be routed to the same datacenter.
(For example, if the user’s desktop computer uses the home broadband connec‐
tion and their mobile device uses the cellular data network, the devices’ network
routes may be completely different.) If your approach requires reading from the
leader, you may first need to route requests from all of a user’s devices to the
same datacenter. 


### Monotonic reads

Our second example of an anomaly that can occur when reading from asynchronous
followers is that it’s possible for a user to see things moving backward in time.

This can happen if a user makes several reads from different replicas. For example,
User 2345 making the same query twice, first to a follower with little
lag, then to a follower with greater lag. (This scenario is quite likely if the user
refreshes a web page, and each request is routed to a random server.) The first query
returns a comment that was recently added by user 1234, but the second query
doesn’t return anything because the lagging follower has not yet picked up that write.
In effect, the second query is observing the system at an earlier point in time than the
first query. 

**Monotonic reads** is a guarantee that this kind of anomaly does not happen. It’s a
lesser guarantee than strong consistency, but a stronger guarantee than eventual con‐
sistency. When you read data, you may see an old value; monotonic reads only means
that if one user makes several reads in sequence, they will not see time go backward—
i.e., they will not read older data after having previously read newer data.

One way of achieving monotonic reads is to make sure that each user always makes
their reads from the same replica (different users can read from different replicas).
For example, the replica can be chosen based on a hash of the user ID, rather than
randomly. However, if that replica fails, the user’s queries will need to be rerouted to
another replica. 

### Consistent prefix reads

. This guarantee says that if a sequence of writes happens in a certain order,
then anyone reading those writes will see them appear in the same order.

## Multi leader replication

A natural extension of the leader-based replication model is to allow more than one
node to accept writes. Replication still happens in the same way: each node that pro‐
cesses a write must forward that data change to all the other nodes. We call this a
multi-leader configuration (also known as master–master or active/active replication).

### Use Cases for Multi-Leader Replication

- **Multi-datacenter operation**
In a multi-leader configuration, you can have a leader in each datacenter. Within each datacenter, regular leader–
follower replication is used; between datacenters, each datacenter’s leader replicates
its changes to the leaders in other datacenters.

- **Clients with offline operation**
Another situation in which multi-leader replication is appropriate is if you have an
application that needs to continue to work while it is disconnected from the internet.

- **Collaborative editing**
Real-time collaborative editing applications allow several people to edit a document
simultaneously. For example, Etherpad and Google Docs allow multiple
people to concurrently edit a text document or spreadsheet.

We don’t usually think of collaborative editing as a database replication problem, but
it has a lot in common with the previously mentioned offline editing use case. When
one user edits a document, the changes are instantly applied to their local replica (the
state of the document in their web browser or client application) and asynchronously
replicated to the server and any other users who are editing the same document.

If you want to guarantee that there will be no editing conflicts, the application must
obtain a lock on the document before a user can edit it. If another user wants to edit
the same document, they first have to wait until the first user has committed their
changes and released the lock. This collaboration model is equivalent to single-leader
replication with transactions on the leader.
However, for faster collaboration, you may want to make the unit of change very
small (e.g., a single keytroke) and avoid locking. This approach allows multiple users
to edit simultaneously, but it also brings all the challenges of multi-leader replication,
including requiring conflict resolution

### Handling write conflicts

The biggest problem with multi-leader replication is that write conflicts can occur,
which means that conflict resolution is required.

#### Synchronous versus asynchronous conflict detection

In principle, you could make the conflict detection synchronous—i.e., wait for the
write to be replicated to all replicas before telling the user that the write was success‐
ful. However, by doing so, you would lose the main advantage of multi-leader repli‐
cation: allowing each replica to accept writes independently. If you want synchronous
conflict detection, you might as well just use single-leader replication.

#### Conflict avoidance

The simplest strategy for dealing with conflicts is to avoid them: if the application can
ensure that all writes for a particular record go through the same leader, then con‐
flicts cannot occur. Since many implementations of multi-leader replication handle
conflicts quite poorly, avoiding conflicts is a frequently recommended approach.

For example, in an application where a user can edit their own data, you can ensure
that requests from a particular user are always routed to the same datacenter and use
the leader in that datacenter for reading and writing. Different users may have differ‐
ent “home” datacenters (perhaps picked based on geographic proximity to the user),
but from any one user’s point of view the configuration is essentially single-leader.

#### Converging toward a consistent state

A single-leader database applies writes in a sequential order: if there are several
updates to the same field, the last write determines the final value of the field.
In a multi-leader configuration, there is no defined ordering of writes, so it’s not clear
what the final value should be.

There are various ways of achieving convergent conflict resolution:
- Give each write a unique ID (e.g., a timestamp, a long random number, a UUID,
or a hash of the key and value), pick the write with the highest ID as the winner,
and throw away the other writes. If a timestamp is used, this technique is known
as last write wins (LWW). Although this approach is popular, it is dangerously
prone to data loss
- Give each replica a unique ID, and let writes that originated at a highernumbered replica always take precedence over writes that originated at a lowernumbered replica. This approach also implies data loss.
- Somehow merge the values together—e.g., order them alphabetically and then
concatenate them 
- Record the conflict in an explicit data structure that preserves all information,
and write application code that resolves the conflict at some later time (perhaps
by prompting the user).

#### Custom conflict resolution logic

- **On write**
As soon as the database system detects a conflict in the log of replicated changes,
it calls the conflict handler. For example, Bucardo allows you to write a snippet of
Perl for this purpose. This handler typically cannot prompt a user—it runs in a
background process and it must execute quickly.

- **On read**
When a conflict is detected, all the conflicting writes are stored. The next time
the data is read, these multiple versions of the data are returned to the applica‐
tion. The application may prompt the user or automatically resolve the conflict,
and write the result back to the database. CouchDB works this way, for example.

## Leaderless replication

Some data storage systems take a different approach, abandoning the concept of a
leader and allowing any replica to directly accept writes from clients. Riak, Cassandra, and Voldemort are open source datastores with leaderless
replication models inspired by Dynamo, so this kind of database is also known as
Dynamo-style.

### Writing to the Database When a Node Is Down

Imagine you have a database with three replicas, and one of the replicas is currently
unavailable—perhaps it is being rebooted to install a system update. In a leader-based
configuration, if you want to continue processing writes, you may need to perform a
failover.
On the other hand, in a leaderless configuration, failover does not exist. Suppose the client (user 1234) sends the write to all three replicas in par‐
allel, and the two available replicas accept the write but the unavailable replica misses
it. Let’s say that it’s sufficient for two out of three replicas to acknowledge the write:
after user 1234 has received two ok responses, we consider the write to be successful.
The client simply ignores the fact that one of the replicas missed the write.

### Read repair and anti-entropy

The replication scheme should ensure that eventually all the data is copied to every
replica. After an unavailable node comes back online, how does it catch up on the
writes that it missed?

- **Read repair**
When a client makes a read from several nodes in parallel, it can detect any stale
responses. For example, a user 2345 gets a version 6 value from rep‐
lica 3 and a version 7 value from replicas 1 and 2. The client sees that replica 3
has a stale value and writes the newer value back to that replica. This approach
works well for values that are frequently read.

- **Anti-entropy process**
In addition, some datastores have a background process that constantly looks for
differences in the data between replicas and copies any missing data from one
replica to another. Unlike the replication log in leader-based replication, this
anti-entropy process does not copy writes in any particular order, and there may
be a significant delay before data is copied.

### Quorums for reading and writing

If there are n replicas, every write must be confirmed by w nodes to
be considered successful, and we must query at least r nodes for each read. (In our
example, n = 3, w = 2, r = 2.) As long as w + r > n, we expect to get an up-to-date
value when reading, because at least one of the r nodes we’re reading from must be
up to date. Reads and writes that obey these r and w values are called quorum reads
and writes

### Detecting Concurrent Writes

Dynamo-style databases allow several clients to concurrently write to the same key,
which means that conflicts will occur even if strict quorums are used. The situation is
similar to multi-leader replication

- **Last write wins (discarding concurrent writes)**
One approach for achieving eventual convergence is to declare that each replica need
only store the most “recent” value and allow “older” values to be overwritten and dis‐
carded. Then, as long as we have some way of unambiguously determining which
write is more “recent,” and every write is eventually copied to every replica, the repli‐
cas will eventually converge to the same value. 
**If losing data is not acceptable, LWW is a poor choice for conflict resolution.**

- **The “happens-before” relationship and concurrency**
An operation A happens before another operation B if B knows about A, or depends
on A, or builds upon A in some way. Whether one operation happens before another
operation is the key to defining what concurrency means. In fact, we can simply say
that two operations are concurrent if neither happens before the other

- **Algorithm to determine happens before relationship**

The server can determine whether two operations are concurrent by looking
at the version numbers—it does not need to interpret the value itself. The algorithm works as follows:

    1. The server maintains a version number for every key, increments the version
    number every time that key is written, and stores the new version number along
    with the value written.

    2. When a client reads a key, the server returns all values that have not been over‐
    written, as well as the latest version number. A client must read a key before
    writing.

    3. When a client writes a key, it must include the version number from the prior
    read, and it must merge together all values that it received in the prior read.

    4.When the server receives a write with a particular version number, it can over‐
    write all values with that version number or below (since it knows that they have
    been merged into the new value), but it must keep all values with a higher ver‐
    sion number (because those values are concurrent with the incoming write).









