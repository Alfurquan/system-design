# 🧩 Exercise 1: Distributed Key-Value Store (like DynamoDB)

## 📘 Problem Statement

You're designing a distributed key-value store that needs to support:

- Billions of unique keys  
- High read and write throughput  
- Horizontal scalability (nodes can be added/removed dynamically)  
- Low-latency operations (sub-10ms target)  
- Fault tolerance (some nodes may go down)  
- Basic operations: `put(key, value)`, `get(key)`

### The store should:

- Evenly distribute keys and load  
- Minimize rebalancing effort when scaling  
- Avoid hotspots even if some keys are accessed more than others  

---

## 🎯 Question

Design a partitioning strategy for this key-value store.

- What method would you use? (hash, range, directory, etc.)  
- How would you handle **rebalancing** and **node failures**?  
- How would you deal with **hot keys**?



## Solution

- What method would you use? (hash, range, directory, etc.)

Since it is key value store, we can use hash method to partition the data. We will have partitions for hash ranges, key goes to a hash function which generates a hash value, and then based on what range it falls in, we assign it to the corresponding partition for that range.

- How would you handle **rebalancing** and **node failures**?  

For rebalancing, we can go with dynamic partitioning. An advantage of dynamic partitioning is that the number of partitions adapts to the
total data volume. If there is only a small amount of data, a small number of parti‐
tions is sufficient, so overheads are small; if there is a huge amount of data, the size of
each individual partition is limited to a configurable maximum.

Node failues we will handle by making use of replication and storing each partition on multiple nodes so that if one node for a partition goes down, other node can serve requests for that partition.

- How would you deal with **hot keys**?

We can deal with **hot keys**, by making salting the keys. We can take a compound key by attaching timestamp to the key and then distributing it across the partitions. This way the hot keys requets will be evenly distributed across the partitions.


## Improvements

-  What method would you use? (hash, range, directory, etc.)

You mentioned “ranges” — it would help to clarify whether you're doing modulo-based partitioning (hash(key) % N) or using consistent hashing over a ring.

In large-scale systems like DynamoDB, consistent hashing is preferred to reduce rebalancing overhead.

💬 Improvement Tip:

Say: “We’ll use consistent hashing with virtual nodes to map keys to partitions. This allows us to scale by adding/removing nodes with minimal reshuffling of keys.”

- How would you handle **rebalancing** and **node failures**?  
    - The term dynamic partitioning is a bit vague. Are you referring to auto-splitting partitions when they grow large?
    - You missed explicitly mentioning re-replication after a node fails, or using quorum-based replication like in Dynamo (W/R/N).
    - You could have added how partition ownership metadata is managed (e.g., via a distributed metadata service).

💬 Improvement Tip:

“We'll use replication factor of 3, with partitions stored on multiple nodes. On node failure, a gossip or membership protocol detects failure, and a replica is promoted. Partition metadata is updated accordingly.”

- How would you deal with **hot keys**?
    
    ⚠️ Concern:
    - Appending a timestamp to the key will break idempotency for a key-value store (the same key becomes multiple keys).
    - It also makes get(key) impossible — which violates basic functionality of the system (you’d never know what the key is anymore).

💬 Correct Approach:

“For hot keys, we’ll use key salting with multiple ‘virtual keys’ (e.g., user123_0, user123_1, etc.). Writes are sharded randomly across them. Reads use a fan-out read across all salted variants and aggregate results. We can track mapping of hot keys using a control structure or predefine the hot set.”





