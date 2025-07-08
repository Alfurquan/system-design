# 🧪 Exercise 2: Design a Time-Series Database (like InfluxDB or Prometheus)

## 📘 Problem Statement

You're designing a time-series database to store metrics from IoT devices.

Each device sends timestamped data points like CPU usage, temperature, memory stats, etc.

The system must support:

- High write throughput (millions of writes/sec)  
- Efficient reads by time range and device  
- Scalability to billions of data points from thousands of devices  
- Real-time dashboards showing the last X minutes of data  
- Long-term queries for trends (e.g., CPU usage over 6 months)

---

## 🎯 Design Task

Design the partitioning strategy for this time-series database.

Please explain:

- What partitioning method you'd choose and **why**  
- How you’d structure the **partition key** (fields, granularity)  
- How you’d handle **skew** if some devices send a lot more data  
- Any special consideration for **time-based queries** or **data retention**

---

## Solution

- What partitioning method you'd choose and **why**  

Hash based partitioning to distribute the load evenly across paritions and nodes.

-  How you’d structure the **partition key** (fields, granularity)  

Parition key will be of form ServerName and timestamp. We will salt the server name with random numbers from say 0-9 to handle hot keys and then hash the salted value to get the partition, We will store the data in sorted order of timestamp to support time based queries.

- How you’d handle **skew** if some devices send a lot more data  

 We will salt the server name with random numbers from say 0-9 to handle hot keys and then hash the salted value to get the partition. This way will handle the skew and distribute requests evenly across the partitions.

- Any special consideration for **time-based queries** or **data retention**

**time-based queries**

We could prefix each timestamp with the sensor name so that the partitioning is first by sensor name and
then by time. Assuming you have many sensors active at the same time, the write
load will end up more evenly spread across the partitions. Now, when you want to
fetch the values of multiple sensors within a time range, you need to perform a sepa‐
rate range query for each sensor name.

**data retention**

Since we already partion by sensor name and then by time, we can drop all partitions for a sensor whose time stamps have passed the retention period time.

---

## Improvements

- What partitioning method you'd choose and **why**  

🧠 Suggestions:

In time-series DBs, range or time bucketing partitioning is often preferred over raw hashing to enable efficient time-bound queries and retention.

You could say:

"We combine hash-based partitioning of a salted server name for load balancing within a time bucket, and partition data by time window (e.g., daily/hourly buckets) for query efficiency and retention."

-  How you’d structure the **partition key** (fields, granularity)  

⚠️ Concern:

If you hash the salted key to choose the partition, your data becomes non-contiguous by time — which hurts time range scans (they may span many partitions).

If the system supports it, better to partition by time window first, then distribute load using salt + hash within that time bucket.

🧠 Suggested Approach:

"We partition by (sensor_id, day) or (device_id, hourly_bucket) and use salt to distribute writes within the bucket. The data within each partition is sorted by timestamp for efficient range scans."

- How you’d handle **skew** if some devices send a lot more data  

🧠 Additional Thought:

You could mention that you’ll detect hot devices dynamically (using metrics) and increase the salt space (e.g., 0–99) adaptively.

- Any special consideration for **time-based queries** or **data retention**

⚠️ Concerns:

You're describing a layout where sensor comes first — which is okay for per-sensor queries, but bad for time-range queries across all sensors (e.g., system-wide dashboards).

You're not fully leveraging time-bucketing, which helps with query and retention together.

🧠 Tip:

Consider this structure:

Partition key: (sensor_id, time_bucket)

Sort key: timestamp

Enables: Efficient per-sensor time range scan; easy retention by dropping time buckets





