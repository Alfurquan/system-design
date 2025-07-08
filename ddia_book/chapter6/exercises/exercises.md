## 🧩 1. Design a Scalable Distributed Key-Value Store (like DynamoDB)

**Problem Statement:**  
You're asked to design a distributed key-value store that supports high availability, low latency, and scales to billions of keys across thousands of nodes.

**Goals:**
- Choose a suitable partitioning strategy for keys.
- Handle node addition/removal with minimal data reshuffling.
- Ensure fault tolerance and replication across partitions.

**Challenges:**
- How do you avoid hot partitions from popular keys?
- How would consistent hashing help in minimizing rebalancing?
- Can you support both point lookups and range scans?

---

## 🧮 2. Design a Time-Series Database (like InfluxDB or Prometheus)

**Problem Statement:**  
Build a time-series DB that stores metrics per device (e.g., CPU usage per IoT device) with timestamped entries.

**Goals:**
- Efficiently partition large volumes of timestamped data.
- Support both recent real-time queries and long-term batch queries.
- Optimize for write-heavy workload.

**Challenges:**
- Which partition key to choose: device_id, time window, or both?
- How do you prevent skew if some devices report more often?
- What happens if all writes come in for the latest time range?

---

## 🧑‍💻 3. Design Twitter-like Feed Service

**Problem Statement:**  
Design the backend for Twitter where users post tweets and see a feed of tweets from people they follow.

**Goals:**
- Store tweets efficiently and partition user timelines.
- Support fast feed reads and writes at scale.

**Challenges:**
- Do you partition by user ID or tweet ID?
- How to prevent hotspots from celebrity users?
- How to handle follower fan-out efficiently across partitions?

---

## 🎥 4. Design a Scalable Video Metadata Store (like YouTube Catalog)

**Problem Statement:**  
Build a metadata storage service for billions of videos. Each video has info like title, tags, creator, views, etc.

**Goals:**
- Partition the metadata store so it supports fast reads/writes.
- Optimize for creator and tag-based lookups.

**Challenges:**
- Partition by video ID vs creator ID vs tags — tradeoffs?
- How do you support multi-key or secondary index queries (e.g., top videos by tag)?
- How would you handle rebalancing when new creators become popular?

---

## 📊 5. Design a Real-Time Analytics Dashboard (e.g., Google Analytics)

**Problem Statement:**  
You need to store and process billions of page views and user events for multiple clients in real-time and serve dashboards.

**Goals:**
- Partition data so writes and queries are balanced.
- Support range queries by time and filters by client.

**Challenges:**
- Partition by client ID, page ID, or time bucket?
- How to reduce the impact of skew if one client gets 90% of traffic?
- Support both real-time streaming and batch aggregations across partitions.

---

## 🛒 6. Design an E-Commerce Order System

**Problem Statement:**  
You’re building a backend system for managing customer orders and want to distribute the order data for scalability and fault tolerance.

**Goals:**
- Support high write volume and order lookup by customer or order time.
- Enable partitioned storage and indexing for performance.

**Challenges:**
- Partition by customer ID or order ID?
- What if a few large customers generate huge order volume?
- How do you query for orders within a time range across all customers?

---

## 📈 7. Simulate Partitioning and Rebalancing (Coding Exercise)

**Problem Statement:**  
Write a simulation of:
- Hash partitioning
- Consistent hashing with virtual nodes

**Goals:**
- Generate N keys and assign them to M partitions.
- Visualize distribution of keys across partitions.
- Add/remove a partition node and see how many keys move.

**Challenges:**
- Compare how consistent hashing reduces rebalancing vs modulo hashing.
- Show effect of hot keys and how salting (key randomization) changes the distribution.
