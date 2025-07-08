# 📊 Exercise 5: Design a Real-Time Analytics Dashboard (e.g., Google Analytics)

## 📘 Problem Statement

You're tasked with designing a system to store and process **billions of page views** and **user events** in real-time for multiple clients, with a goal of serving **interactive dashboards**.

You’ll need to:

- Partition data to ensure both writes and queries are efficient.
- Support **range queries** (e.g., get views from the last 24 hours).
- Filter data by client (e.g., “show data for Client A”).
- Aggregate data in real-time and also support batch aggregations for broader metrics.

---

## 📊 System Requirements

- **High Throughput:** You need to ingest millions of events per second.
- **Low Latency:** The dashboard needs to be interactive with near real-time performance.
- **Partitioning:** You need to partition data for efficient writes and queries.
- **Scalability:** The system should scale to handle billions of events from many clients.
- **Fault Tolerance:** Data should be replicated to ensure reliability.
- **Aggregation:** Support both real-time streaming aggregation and batch aggregation across partitions.

---

## 🚩 Challenges

### Partitioning Strategy:

- Should you partition by **client ID**, **page ID**, or **time bucket**?
- How do you handle **skew** when one client gets most of the traffic?

### Real-Time and Batch Processing:

- How would you process the events in **real-time** while also maintaining accurate **batch aggregation**?

### Query Efficiency:

- How do you optimize for **range queries by time** and **filters by client**?

---

## 🎯 Your Task

1. **What partitioning strategy would you use?**

2. **How would you handle skew when one client gets 90% of the traffic?**

3. **How would you process the data in real-time and support batch aggregations?**

4. **How would you ensure scalability and fault tolerance in your system?**

---

## Solution

Before answering these questions, let's consider the data structure we will be working with. Each event might look like this:

```json
{
    "eventId": "abc123",
    "clientId": "client456",
    "pageId": "page789",
    "timestamp": "2023-10-01T12:00:00Z",
    "eventType": "page_view",
    "metadata": {
        "userId": "user101",
        "sessionId": "session202",
        "duration": 120
    }
}
```

### 1. Partitioning Strategy
For this real-time analytics dashboard, I would use a **composite partitioning strategy** that combines `client_id` and `time_bucket`. This allows for efficient querying by client while also enabling range queries by time.
I would use a hash-based partitioning on `client_id` to ensure even distribution across partitions and use a time-based partitioning strategy (e.g., daily or hourly buckets) to allow for efficient range queries.

### 2. Handling Skew

For handling skew when one client gets 90% of the traffic, I would implement salting techniques. This could involve appending a random suffix to the `client_id` or using a hash of the `client_id` to create sub-partitions. This way, even if one client has a lot of traffic, it will be distributed across multiple partitions, reducing the risk of hotspots.

### 3. Real-Time and Batch Processing
To process data in real-time, I would use a stream processing framework like Apache Kafka or Apache Flink. This would allow me to ingest events as they come in and perform real-time aggregations (e.g., counting page views, calculating session durations) using windowing techniques.
For batch processing, I would periodically aggregate the data using a batch processing framework like Apache Spark.
This would allow me to compute broader metrics (e.g., daily active users, total page views) across all partitions.

### 4. Scalability and Fault Tolerance
To ensure scalability, I would design the system to be horizontally scalable. This means adding more partitions as needed to handle increased traffic. I would also use a distributed database or data warehouse that supports partitioning and replication, such as Apache Cassandra or Amazon Redshift.
For fault tolerance, I would replicate data across multiple nodes and use a consensus algorithm (like Raft or Paxos) to ensure consistency. Additionally, I would implement data backups and use a distributed file system (like HDFS or S3) to store raw event data for recovery in case of failures.
---