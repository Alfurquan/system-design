# Problem Statements

## 1. Load Balancer

### ✅ Problem Statement
Design and implement a simulation of a load balancer that distributes incoming HTTP requests across a pool of backend servers. Your balancer should support:

- Round-robin routing  
- Random selection  
- Consistent hashing  
- Simulate backends going offline and recovering  
- **Bonus**: Implement active health checks for servers

### 💡 Mindset Shift
Instead of just implementing, ask:

- Why does consistent hashing reduce rebalancing?  
- When should you use client-side load balancing vs a centralized gateway like Envoy?

### 📚 Learning Objective
Understand traffic distribution strategies, fault tolerance, and how load balancers affect system resilience.

---

## 2. In-Memory Caching (LRU + TTL)

### ✅ Problem Statement
Create a simple in-memory cache that supports:

- `get(key)`, `put(key, value, ttl)`  
- Least Recently Used (LRU) eviction
- Least Frequently Used (LFU) eviction
- Time-based expiration (TTL)  
- **Optional**: Auto-cleanup of expired keys

### 💡 Mindset Shift
Focus on:

- Why does cache eviction policy matter for user experience or system performance?  
- Where would you place this cache — browser, edge, DB layer?

### 📚 Learning Objective
Grasp how caching improves latency, scalability, and how eviction/expiration strategies affect system design.

---

## 3. Data Sharding

### ✅ Problem Statement
Simulate a system where a dataset is partitioned across N storage nodes using:

- Range-based sharding  
- Hash-based sharding  
- Route read/write operations to the right shard  
- Demonstrate behavior when a shard is added or removed

### 💡 Mindset Shift
Ask:

- What’s the cost of resharding?  
- How does sharding affect consistency and hotspots?

### 📚 Learning Objective
Understand data partitioning, balancing, routing, and real-world issues like re-sharding and key distribution.

---

## 4. Replication

### ✅ Problem Statement
Simulate a replicated write system:

- A leader node receives writes  
- Follower nodes replicate changes with lag  
- Simulate follower crashes, replays, and stale reads  
- Show eventual vs synchronous replication effects

### 💡 Mindset Shift
Explore:

- When does async replication lead to data inconsistency?  
- How would you explain replication lag to a stakeholder?

### 📚 Learning Objective
Internalize consistency guarantees and recovery strategies in replicated systems.

---

## 5. Consistency Models

### ✅ Problem Statement
Implement a basic key-value store with:

- Multiple clients writing to the same key  
- Simulate last-write-wins, vector clocks, or version history  
- Return divergent values for eventual vs strong consistency

### 💡 Mindset Shift
Ask:

- When is eventual consistency “good enough”?  
- How do distributed stores like Cassandra resolve conflicts?

### 📚 Learning Objective
Gain intuition for distributed data consistency, conflict resolution, and causal relationships.

---

## 6. Transactions & 2PC

### ✅ Problem Statement
Simulate a Two-Phase Commit across 3 services:

- Implement a coordinator node  
- Simulate `PREPARE` and `COMMIT/ABORT` messages  
- Show failure at each step (before/after commit)  
- **Bonus**: Add retry logic or simulate network partition

### 💡 Mindset Shift
Ask:

- Why does 2PC block in case of coordinator failure?  
- What are better alternatives (e.g. Saga, idempotent retries)?

### 📚 Learning Objective
Understand distributed transactions, failure modes, and why most systems avoid 2PC.

---

## 7. Message Queue (Kafka-style)

### ✅ Problem Statement
Build a basic message queue with:

- Producers and consumers  
- Support for acknowledgment, retries, and message ordering  
- **Optional**: Partitioned queues and replayable logs

### 💡 Mindset Shift
Ask:

- Why use queues instead of direct calls?  
- What trade-offs exist between RabbitMQ, Kafka, SQS?

### 📚 Learning Objective
Understand message durability, delivery semantics, and event-driven design.

---

## 8. Rate Limiting (Token Bucket)

### ✅ Problem Statement
Implement a token bucket rate limiter:

- Limit: 5 requests per second, burst of 10  
- Add support for per-user rate limiting  
- Drop or delay excess requests

### 💡 Mindset Shift
Ask:

- Why do APIs need burst handling?  
- What happens if the rate limiter itself goes down?

### 📚 Learning Objective
Grasp defensive design to protect services and ensure fair usage.

---

## 9. Data Modeling

### ✅ Problem Statement
Model a Bookstore in:

- PostgreSQL (Relational)  
- MongoDB (Document-based)  
- Neo4j (Graph-based)

Support queries like:

- “All books by an author”  
- “Top co-purchased books”  
- “Most reviewed authors”

### 💡 Mindset Shift
Ask:

- How does query shape drive schema?  
- What trade-offs does denormalization bring?

### 📚 Learning Objective
Learn schema design for different database paradigms and their access patterns.

---

## 10. Key-Value Store Internals

### ✅ Problem Statement
Design a log-structured KV store:

- Append-only write log  
- In-memory index  
- Merge segments (compaction)  
- **Optional**: Implement Bloom filter for fast lookups

### 💡 Mindset Shift
Ask:

- How do LSM-trees help with write-heavy workloads?  
- Why do modern DBs (LevelDB, RocksDB) avoid B-trees?

### 📚 Learning Objective
Understand how high-performance storage engines work internally.

---

## 11. Chunked File Storage

### ✅ Problem Statement
Implement chunked file upload:

- Split large files into 64MB chunks  
- Store chunks across multiple nodes  
- Reconstruct the file in order  
- Handle missing chunks and checksum mismatch

### 💡 Mindset Shift
Ask:

- Why chunk and distribute?  
- How do systems like Dropbox ensure data integrity and deduplication?

### 📚 Learning Objective
Learn how systems like HDFS, GFS, and S3 manage large file storage.

---

## 12. Job Scheduler

### ✅ Problem Statement
Design a job queue system:

- FIFO queue for incoming jobs  
- Support for retries with backoff  
- Priority jobs  
- **Optional**: Cron-style recurring jobs

### 💡 Mindset Shift
Ask:

- How would I scale this for 10,000 jobs/min?  
- What happens if the scheduler restarts during a job?

### 📚 Learning Objective
Understand task orchestration, retries, and eventual execution guarantees.

---

## 13. Logging & Monitoring

### ✅ Problem Statement
Create a logging system:

- Log events of varying severity  
- Batch upload logs to a file or store  
- Raise alerts if error count exceeds threshold  
- **Optional**: Histogram of event frequency

### 💡 Mindset Shift
Ask:

- Which logs are useful for debugging, which for alerting?  
- How do you set thresholds or detect anomalies?

### 📚 Learning Objective
Understand observability fundamentals — logs, metrics, traces, alerts.

---

## 14. JWT Authentication

### ✅ Problem Statement
Simulate a simple auth system:

- Generate JWT for users with roles  
- Validate JWT on every request  
- Handle expiration and token refresh  
- **Optional**: Simulate blacklist/revocation

### 💡 Mindset Shift
Ask:

- Why is stateless auth scalable?  
- What are risks (e.g. XSS, token leakage)?

### 📚 Learning Objective
Understand stateless authentication, its trade-offs, and security implications.

---

## 15. API Gateway

### ✅ Problem Statement
Create an API Gateway that:

- Routes requests to different services  
- Adds auth headers  
- Applies rate limits and logging  
- **Optional**: Aggregate responses from multiple services

### 💡 Mindset Shift
Ask:

- How does a gateway improve security and observability?  
- Where does it fit in service mesh architecture?

### 📚 Learning Objective
Learn centralized request routing, auth, and edge-layer protections.

---

## 16. Circuit Breaker

### ✅ Problem Statement
Simulate service calls where:

- A downstream service fails randomly  
- After 5 failures, the circuit “opens”  
- After timeout, it moves to half-open and retries

### 💡 Mindset Shift
Ask:

- How does this protect upstream services?  
- How do retry/backoff/circuit-breaker interact?

### 📚 Learning Objective
Understand graceful degradation and failure isolation.
