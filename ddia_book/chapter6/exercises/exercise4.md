# 🎥 Exercise 4: Design a Scalable Video Metadata Store (like YouTube Catalog)

## 📘 Problem Statement

You’re building a metadata service for a YouTube-like video platform.

Each video has:

- `video_id`  
- `title`  
- `description`  
- `tags` (e.g., `"music"`, `"sports"`)  
- `creator_id`  
- `views`  
- `upload_timestamp`  

---

## 📊 Goals

- Store **billions** of videos' metadata  
- Support **fast lookup by video ID**  
- Support **fast queries by creator ID**, e.g., “all videos by Creator X”  
- Support **tag-based browsing**, e.g., “top videos in music”  
- Efficient updates (e.g., views counter increment)  
- Low-latency reads  

---

## 🚩 Challenges

### Partitioning Tradeoffs:

- Partitioning by `video_id` is good for **direct lookup**  
- Partitioning by `creator_id` is better for **listing all of a creator's videos**  
- **Tags are many-to-many** and hard to partition  
- **Hot creators and skew** — some have millions of videos  

### Supporting Queries Like:

- “Top 10 videos by views for tag = music”  
- “Latest 100 videos by creator X”  

---

## 🎯 Your Task

Answer these 4 parts:

1. **What partitioning strategy would you use? Why?**  
2. **How would you support efficient queries by video ID, creator ID, and tag?**  
3. **How would you handle hot creators or popular tags?**  
4. **How would you support multi-key or secondary index queries (like top videos per tag)?**

---

## Solution

Before answering these questions, lets look at a sample of what we will be storing

```json
{
    "videoId": "123sss",
    "title": "My First Video",
    "description": "This is a description of my first video",
    "tags": ["music", "funny"],
    "creatorId": "creator123",
    "views": 1000,
    "uploadTimestamp": "2023-10-01T12:00:00Z"
}

```

### 1. Partitioning Strategy

For this metadata service, I would use a **composite partitioning strategy** that combines `creator_id` and `video_id`. This allows for efficient lookups by both creator and video ID while also enabling fast access to all videos by a specific creator. I will use hash based partitioning on video_id to ensure even distribution across partitions, while also allowing for efficient range queries on creator_id througn the use of a secondary index that will also be partitioned by creator_id. 

### 2. Supporting Efficient Queries

To support efficient queries by video ID, creator ID, and tag, I would implement the following:
- **Primary Key**: Use a composite primary key of `creator_id` and `video_id`. This allows for fast lookups by video ID and efficient retrieval of all videos by a specific creator.
- **Secondary Indexes**:
    - **Creator Index**: A secondary index on `creator_id` to quickly retrieve all videos by a specific creator.

- **Tag lookup table**: A separate table or index that maps tags to video IDs, allowing for efficient tag-based browsing. Since there is many to many relationship between tags and videos, this table would store each tag as a key and a list of video IDs as the value.

- **Lookup by Video ID**: Use the primary key to directly access a video by its `video_id`.
- **Lookup by Creator ID**: Use the secondary index to retrieve all videos for a specific.
- **Tag-based Browsing**: Use the tag lookup table to find all videos associated with a specific tag.

### 3. Handling Hot Creators or Popular Tags

To handle hot creators or popular tags, I would implement the following strategies:

- **Hot creators**: 
    - I will partition the data by `creator_id` and use a sharding strategy to distribute the load across multiple partitions. Will use salting by adding a random suffix to the `creator_id` to avoid hotspots.
    - Implement caching for frequently accessed creators to reduce load on the database.

- **Popular tags**: 
    - Use a separate partition for popular tags to ensure they are not affected by the load of less popular tags.
    - Implement a caching layer for popular tags to speed up access and reduce database load.


### 4. Supporting Multi-Key or Secondary Index Queries

To support multi-key or secondary index queries, such as retrieving the top videos per tag, I would implement the following:
- **Secondary Indexes**: Create secondary indexes for tags that allow for efficient retrieval of videos by tag. This index would map tags to video IDs, enabling fast lookups.
- **Top Videos Query**: For queries like “Top 10 videos by views for tag = music”, I would:
    - Use the tag lookup table to get all video IDs associated with the tag "music".
    - Retrieve the metadata for these videos and sort them by views to get the top 10.
- **Caching**: Implement caching for frequently accessed queries, such as top videos by tag, to reduce database load and improve response times.

---

## Improvements

### 1. Partitioning Strategy

🧠 Suggestions:

You could clarify how the secondary index will be stored. For example, will it be separate from the main table or stored in a distributed index system like Elasticsearch? This is important when discussing scalability and data locality for efficient queries.

Example:
"I will maintain the secondary index as a distributed index (e.g., Elasticsearch or Lucene) for efficient searches across creator_id."

### 2. Supporting Efficient Queries

🧠 Suggestions:

For tag-based queries, you’ve described using a lookup table that maps tags to video IDs, which is a good idea. You may also want to mention denormalization or materialized views as a strategy to speed up queries (instead of just having a direct table lookup).

Example:
“To ensure quick tag-based queries, I will denormalize the tag-video relationships into a materialized view that stores top tags with pre-aggregated video counts. This reduces query time when accessing highly frequent tags.”

### 3. Handling Hot Creators or Popular Tags

🧠 Suggestions:

It would be helpful to discuss how to detect and prioritize hot creators dynamically. For example, through a metrics system that monitors the number of views per creator.

Example:
"I would introduce a metrics system that detects creators with spikes in views or activity. These creators will be dynamically moved to dedicated partitions with auto-scaling to handle the increased load.”

### 4. Supporting Multi-Key or Secondary Index Queries

🧠 Suggestions:

For top videos by tag, you could also discuss how aggregation could be handled. If the volume of videos grows large, it's better to pre-aggregate data.

Additionally, you may want to consider how the secondary index is kept up-to-date as videos accumulate views — possibly through batch processing or real-time updates.

Example:
“For top video queries, I will maintain a top N cache or pre-aggregated view that calculates the top videos by views per tag, updated periodically or in real-time using event streaming (e.g., Kafka).”

## Learnings 

### Materialized views

Materialized views are a database optimization technique used to speed up query performance by precomputing and storing the results of a complex query. Instead of calculating the result on the fly every time the query is executed, a materialized view stores the computed data in a persistent form.

#### 📘 What is a Materialized View?

- A materialized view is a precomputed table that holds the results of a query.

- The view is **"materialized"** (stored) physically, which means the results of the query are saved in a persistent table, unlike a regular view, which is a virtual representation of the data and is calculated each time it’s accessed.

- Materialized views are typically used for complex aggregations, join operations, or expensive calculations that need to be queried frequently, especially when working with large datasets.

#### 🧠 Key Benefits of Materialized Views

- Faster Query Performance:
    Since the results are already computed and stored, retrieving data from a materialized view is much faster compared to computing the result every time you query it.

- Particularly useful for aggregation-heavy queries (e.g., "Top 10 videos by views" or "Summarize views per tag").

- Reduced Load on the Database:
    By precomputing results, you avoid repetitive calculations and reduce the overall load on your database when querying for aggregated data.

- Optimized for Reporting and Analytics:
    Materialized views are often used in analytics-based systems where performance is crucial, such as data warehousing and reporting systems.

#### ⚡ How Materialized Views Work

- Initial Query:
    A materialized view is created based on a query. For example, a query that aggregates the top videos by views, grouped by tags.
    The database runs the query and stores the result in a physical table.

- Query Execution:
    When a query is made to the materialized view, the database doesn’t need to recalculate the results — it simply returns the precomputed data.

- Refreshing the View:
    Materialized views need to be refreshed periodically to ensure they remain consistent with the source data.
    The refresh can be:
    - Manual: Triggered at specific times.
    - Automatic: Refreshed on a regular interval or based on changes in the underlying data.

#### 📊 Example Use Case

In the  Video Metadata Store problem:

- Query: "Top 10 videos by views for tag = music."

- Challenge: Continuously calculating "Top 10" for every tag across millions of videos is expensive and time-consuming.

##### Materialized View Solution:

- Precompute the top 10 videos for each tag periodically (e.g., once a day).

- Store the result in a materialized view.

- For tag-based queries, fetch the results directly from the materialized view instead of recalculating them each time.


