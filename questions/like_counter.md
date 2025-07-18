# 📌 Problem Statement: Design a Distributed Likes Counter System

## Background

You are tasked with designing the backend system for a global social media platform like Instagram, YouTube, or TikTok. Users can "like" various entities such as posts, videos, or comments. These likes need to be recorded and the current like count must be accurately shown on the UI with low latency and high availability

## Answer

1. **Functional requirements (Core requirements)**
    - Users can like a post
    - If they like a post, like count should increase
    - If they like a post again, this should unlike the post and like count should decrease
    - Users should be able to see the like counts on the post.
  
2. **Non functional requirements**
    - High Throughput: The system should handle thousands of likes per second, including spikes from viral content  (say a celebrity’s post).
    - Scalability: The system must be horizontally scalable (able to add servers/nodes to handle growth)
    - Highly Available: A failure in one component should not bring down the whole “likes” functionality.
    - Low Latency: Liking a post should feel instant. The displayed count can lag slightly but should stay reasonably up to date.
    - Consistency: We aim for eventual consistency — brief discrepancies in counts are acceptable, but they must reconcile quickly. Strong consistency is nice-to-have, not a must.
    - Durability: No likes should be lost, even during failures. Every like must be recorded persistently.
    - Idempotency: A user’s like should count only once, even if the action is retried or duplicated.
    - Analytics-Friendly: The system should support analytics use cases like identifying trending posts (e.g., most-liked posts in the last hour).

3. **Optional Extensions**
   - Show top-N liked posts in the last X minutes globally or within a region.
   - Expose an analytics dashboard for likes over time (e.g., likes per hour/day per region).
  
4. **Core entities**
    These will be the core entities of the system
    - User: User of the system

        ```json
        id: Id of the user
        name: Name of the user
        email: Email of the user
        bio: Bio of user
        ... other fields
        ```

    - Post: Post which they like/unlike
  
        ```json
        id: Id of the post
        title: Title of the post
        content: Content of the post
        imageURLs: List of Image URLs of the post stored in object storage like S3.
        authorId: User id of the author
        createdAt: Timestamp when the post was created
        likesCount: Count of likes
        ```

    - Likes: Like entity
  
        ```json
        post_id: Id of the post which was liked
        user_id: Id of the user who liked the post
        timestamp: Time when post was liked
        ```

5. **APIs(Simple ones to start, we will evolve)**
    - Like a post

    ```json
    POST /posts/{id}/likes

    Response
    200 OK
    ```

    - View all likes

    ```json
    GET /posts/{id}/likes

    Response
    200 OK
    [
        {
            postId: <ID of post>
            likeCount: <count of likes>
        }
    ]
    ```

6. **High level design**
    For the design, we will begin with simple single node design and then gradually move to distributed architecture.

    **6.1 Basic Single-Database Design**

    Let’s start with the most straightforward solution — storing likes in a single relational database.
    We create a Likes table with columns like:
    - post_id
    - user_id
    - timestamp
    - (optional) id (auto-incremented)
  
    Every time a user likes a post, we insert a new row into this table.
    To get the total likes for a post, we simply run:

    ```SQL
    SELECT COUNT(1) FROM Likes WHERE post_id = X;
    ```

    On unlike, we can simply delete the corresponding row from the Likes table.

    ```SQL
    DELETE FROM LIKES WHERE post_id = X and user_id = Y;
    ```

    This approach also allows us to easily retrieve the list of users who liked a specific post using a simple query:

    ```SQL
    SELECT user_id FROM Likes WHERE post_id = X;
    ```

    To optimize read queries, we can add an index on post_id, which improves lookup performance as the table grows.

    **High level Architecture**

    <!Insert image here>

    **Drawbacks**

    - Does not scale: Every like triggers a write. With millions of users, the DB quickly becomes a bottleneck. A single SQL database can’t handle that level of write throughput.
    - Expensive Count Queries: Using COUNT(1) on large tables is slow. As posts gain millions of likes, counting them becomes a performance problem — even with indexing.
    - High Latency: Each like inserts a row. Each post view might run a COUNT(1) query. Under load, these operations can slow down the system significantly.
    - Single Point of Failure: If the database goes down, users can’t like posts or see updated counts.

    **6.2 Improving Read Efficiency**

    In our basic design, reading the like count with COUNT(1) is expensive and hits the database hard — especially for popular posts.

    To fix this, we introduce two improvements:

    - Maintain precomputed like counts
    - Use caching for fast reads

    **Precomputed Like Counts**
    Instead of computing the count on every read, we store it alongside the post. This can be done by:

    - Adding a like_count column in the Posts table, or
    - Creating a separate PostLikesCount table with schema: (post_id, like_count)

    Each time a user likes or unlikes a post, we increment or decrement this count. This turns a costly COUNT(1) query into a fast primary-key lookup.

    **Introduce a cache layer**

    We add an in-memory cache (e.g., Redis or Memcached) to store frequently accessed like counts:
    - The app checks the cache first.
    - If the data isn’t in the cache (cache miss), it queries the DB, then stores the result in cache.
    - Subsequent reads for the same post hit the cache, not the DB.

    **High level architecture**
    <! Insert image here>

    **Work flow**

    - On a like
      - We insert row in likes table
      - We increment like count in posts table
      - If both tables, we can wrap them in a transaction
      - Invalidate or update cache entry for the post
    - On reading likes
      - We first check cache, if found we return from cache.
      - If not found on cache, we fetch from DB to cache and return.
  
    **Drawbacks**

    - Cache Inconsistency: When the like count changes in the DB, the cache needs to be updated or invalidated.
    - Write Contention on Hot Posts: Now every like involves two writes (insert in the Likes table + update in the Posts table). For popular posts, the like_count row can become a hotspot, causing lock contention in the DB.
    - Still Single Database: All likes still go through the same DB instance. While reads are faster, we haven’t solved write scalability yet.
    - Eventual Consistency in Caches: If using read replicas or multiple cache layers, some clients may see slightly stale counts due to replication lag or delayed cache updates. Usually acceptable within a short window (milliseconds to seconds).
  
    **6.3 Scaling Out with Database Sharding**

    As traffic and data volume grow, even a powerful single database won’t be enough.
    The next step is sharding — partitioning the data across multiple database servers so no single machine bears all the load.
    Each shard holds a subset of posts and their likes — so reads and writes for a given post only go to its shard.

    **Sharding strategy**
    We shard the data based on post_id, as likes are inherently tied to specific posts. This ensures all likes for a particular post live in the same shard, simplifying reads and writes.

    - Range based Sharding: Posts with post_id from 1–10,000 go to Shard 1, 10,001–20,000 to Shard 2, and so on.
    - Hash based Sharding: shard = hash(post_id) % N
    This spreads posts evenly across N shards.

    **Updated architecture**

    <! Insert image here>

    **Workflow**
    - On like/unlike
        The application determines the appropriate shard using post_id and sends the insert/update to that shard only.
    - On Reading Like Count:
        The application first checks the cache using post_id as the key. If there’s a cache miss, it queries the correct shard to fetch the count

    **Drawbacks**
    - Increased Complexity: The app must know how to find the right shard. This adds logic or requires a routing service.
    - Hot Shard Problem: Real-world traffic is rarely uniform. If one shard ends up with multiple celebrity posts, it could become overwhelmed.
    - Cross-Shard Queries are Hard: Queries like “Top 10 most liked posts” require aggregating data from all shards which adds significant complexity.
    - Duplication and Consistency: We need to ensure that Posts.like_count and entries in Likes remain consistent per shard. This is manageable within a shard but trickier globally.

    **Hot Post Solution: Sharded Counters**
    Even with sharding, a single viral post can overwhelm its shard.
    To handle this, we can shard within a single post. Instead of maintaining one like count per post, we split it into multiple sub-counters.

    Example:
    - For post_id 123, create 10 sub-counters (buckets): counter_0, counter_1, ..., counter_9
    - Each user is assigned to a bucket based on hash(user_id) % 10 and each bucket is stored on a different shard.
    - When user U likes post 123, update the sub-counter:
    bucket = hash(user_id) % 10 → counter_3
    - Total likes = sum of all 10 bucket counts.

    **6.4 Asynchronous Processing with a Message Queue**

    Even with sharding and caching, we're still updating the database synchronously for every like — which limits scalability. To improve both performance and responsiveness, we can decouple the write path using a message queue.

    Instead of writing directly to the database when a user clicks "like," we enqueue the event, respond immediately to the user, and let a background worker update the database later. This gives us eventual consistency — the count updates shortly after the user action, not instantly — but allows the system to handle much higher throughput with lower user-perceived latency.

    **How it works**
    - User Action: Alice clicks “Like” on Post #123.
    - Enqueue the Event: The application creates a message like { post_id: 123, user_id: alice_111, action: "like" }.
    - It sends this to a message queue (e.g., Kafka or RabbitMQ), then immediately returns success to the user.
    - Optimistic UI Update: Alice's app increments the on-screen like count assuming the like will succeed.
    - Consume and Process: A background worker reads the message from the queue, finds the correct database shard for post #123, and:
        - Inserts a record into the Likes table
        - Increments the like_count in the Posts table
        - Optionally updates or invalidates the cache
    - Read Path: When someone views Post #123 later, the updated count is fetched from the cache or DB, reflecting all processed likes.

    **Architecture**
    <! Insert image here>

    **Drawbacks**
    - Eventual Consistency: There's a delay between a user's action and the backend state reflecting it. Counts may lag by a few seconds — usually acceptable in social apps, but it's a trade-off.
    - Operational Complexity: Introducing a message queue and consumer service adds moving parts — more to deploy, monitor, and maintain. We need observability into queue lag, consumer health, and retries.
    - Duplicate Processing Most message queues (like Kafka) use at-least-once delivery. This means the same message might be processed more than once (e.g., if a consumer crashes after DB write but before marking the message as consumed). Without idempotent handling, this can lead to double-counting.
    - Out-of-Order Events: Without partitioning by post_id, likes and unlikes might be processed in the wrong order. We prevent this by ensuring events for a post are routed to the same partition.
    - UI Feedback Loop: Since counts are updated asynchronously, the like count shown may not match the backend immediately. This is usually handled by optimistic UI updates, and users rarely notice.

    **6.5 Ensuring Idempotency, Uniqueness, and Consistency**

    Now that we’ve introduced asynchronous processing using a message queue, it’s critical to handle:
    - Duplicate events
    - Out-of-order like/unlike actions
  
    **The Problem of Duplicates**

    A user may double-click the like button — triggering multiple like events that should count as one.
    In at-least-once delivery systems like Kafka, the same message can be processed more than once. For example:

   - A consumer crashes after updating the DB but before acknowledging the message.
   - Kafka resends the message on restart.
    If we reprocess the like without checking, we’ll double-count it.

    **The Problem of Like/Unlike Ordering**

    Imagine this sequence:
    - User likes a post
    - Seconds later, user unlikes it

    If processed in the right order:

    increment (like) → decrement (unlike) → ✅ count is correct.

    But if events are processed out of order:

    decrement (unlike) before increment → ❌ incorrect count.

    To handle both issues, we maintain a per-user like state using a table:

    ```SQL
    LatestLikeAction (post_id, user_id, action, updated_at)
    Primary Key: (post_id, user_id)
    ```

    - action: TRUE (liked), FALSE (unliked)
    - updated_at: timestamp of the last like/unlike action

    **How Consumers Use This Table**
    - On a "Like" event:
  
      - If no record exists or the user’s last action was “unlike” → Update state to “liked” and increment the count
      - If already “liked” → Ignore (duplicate like)

    - On an "Unlike" event:
  
      - If current state is “liked” → Update to “unliked” and decrement the count
      - If already “unliked” or no record → Ignore (duplicate unlike)

    This makes processing idempotent — multiple retries of the same event have no effect after the first valid state transition.

7. Supporting Analytics and Trending Posts

    Beyond counting likes, social platforms often derive insights from like activity — such as identifying trending content, powering leaderboards, and enabling data-driven decisions. Our architecture, with its event-driven backbone, is well-suited for integrating analytics capabilities without affecting the core counting pipeline.

    **Identifying Trending Posts**

    To build a "Trending Posts" feature, we need to track posts that are receiving a burst of likes in a short time window. Here are a few design options:

    **Streaming Aggregation (Real-Time)**
    We can tap into the same like event stream used by our consumers:

    - Use a stream processor like Kafka Streams, Apache Flink, or Spark Streaming
    - Maintain rolling window counts (e.g., likes in the past 10 minutes or 1 hour)
    - Emit the top N posts for each window periodically (e.g., every minute)

    This enables near real-time trend detection with tunable freshness.

    **Analytics Pipeline Design**

    We can add a parallel consumer to our message queue dedicated to analytics:

    ```shell
    Kafka Topic (post_likes)
    ├── Consumer 1: Like counter (writes to DB)
    └── Consumer 2: Analytics pipeline (writes to S3, BigQuery, or time-series DB)
    ```

8. Leaderboards and Most-Liked Posts

    To support features like:

    - "Top Liked Posts of the Day"

    - "Most Liked of All Time"

    We can:

    - Query the like_count table periodically (if it’s not too large)
    - Or maintain a sorted structure (e.g., Redis sorted set or pre-aggregated table or materialized view)

    A scheduled job can compute and cache leaderboard data every few minutes or hours, storing it in a fast-access DB or cache for display.
