## Caching

### What is caching ?
Caching is a technique used to temporarily store copies of data in high-speed storage layers (such as RAM) to reduce the time taken to access data.

### Why use caching ?
Caching is essential for the following reasons:

- Improved Performance: By storing frequently accessed data in a cache, the time required to retrieve that data is significantly reduced.

- Reduced Load on Backend Systems: Caching reduces the number of requests that need to be processed by the backend, freeing up resources for other operations.

- Increased Scalability: Caches help in handling a large number of read requests, making the system more scalable.

- Cost Efficiency: By reducing the load on backend systems, caching can help lower infrastructure costs.

- Enhanced User Experience: Faster response times lead to a better user experience, particularly for web and mobile applications.

### Types of caching
- In memory cache: In-memory caches store data in the main memory (RAM) for extremely fast access.These caches are typically used for session management, storing frequently accessed objects, and as a front for databases. Eg: Redis and memcached.

- Distributed Cache: A distributed cache spans multiple servers and is designed to handle large-scale systems.

- Client-Side Cache: Client-side caching involves storing data on the client device, typically in the form of cookies, local storage, or application-specific caches.
- Database Cache: Database caching involves storing frequently queried database results in a cache.

- Content delivery network (CDN): CDN is used to store copies of content on servers distributed across different geographical locations.

### Caching strategies

#### **Read-Through Cache**

In the Read Through strategy, the cache acts as an intermediary between the application and the database.
When the application requests data, it first looks in the cache.
If data is available (cache hit), it’s returned to the application.
If the data is not available (cache miss), the cache itself is responsible for fetching the data from the database, storing it, and returning it to the application.

For cache hits, Read Through provides low-latency data access.
But for cache misses, there is a potential delay while the cache queries the database and stores the data. This can result in higher latency during initial reads.

To prevent the cache from serving stale data, a time-to-live (TTL) can be added to cached entries. TTL automatically expires the data after a specified duration, allowing it to be reloaded from the database when needed.

**Read Through caching is best suited for read-heavy applications where data is accessed frequently but updated less often, such as content delivery systems (CDNs), social media feeds, or user profiles.**

#### **Write-Through Cache**

In the Write Through strategy, every write operation is executed on both the cache and the database at the same time. The biggest advantage of Write Through is that it ensures strong data consistency between the cache and the database.

Since the cache always contains the latest data, read operations benefit from low latency because data can be directly retrieved from the cache.

However, write latency can be higher due to the overhead of writing to both the cache and the database.

**Write Through is ideal for consistency-critical systems, such as financial applications or online transaction processing systems, where the cache and database must always have the latest data.**

#### **Write-Around Cache**

Write Around is a caching strategy where data is written directly to the database, bypassing the cache.

The cache is only updated when the data is requested later during a read operation, at which point the Cache Aside strategy is used to load the data into the cache. This approach ensures that only frequently accessed data resides in the cache, preventing it from being polluted by data that may not be accessed again soon.

TTL can be used to ensure that data does not remain in the cache indefinitely. Once the TTL expires, the data is removed from the cache, forcing the system to retrieve it from the database again if needed.

**Write Around caching is best used in write-heavy systems where data is frequently written or updated, but not immediately or frequently read such as logging systems.**

#### **Write-Back Cache**

In the Write Back strategy, data is first written to the cache and then asynchronously written to the database at a later time.

This strategy focuses on minimizing write latency by deferring database writes. The key advantage of Write Back is that it significantly reduces write latency, as writes are completed quickly in the cache, and the database updates are delayed or batched.

However, with this approach, there is a risk of data loss if the cache fails before the data has been written to the database.

**Write Back caching is ideal for write-heavy scenarios where write operations need to be fast and frequent, but immediate consistency with the database is not critical, such as logging systems and social media feeds.**

### Cache eviction policies 

#### **Least recently used (LRU)**
LRU evicts the item that hasn’t been used for the longest time.

The idea is simple: if you haven’t accessed an item in a while, it’s less likely to be accessed again soon.

**Pros**
- Intuitive: Easy to understand and widely adopted.

- Efficient: Keeps frequently accessed items in the cache.

- Optimized for Real-World Usage: Matches many access patterns, such as web browsing and API calls.

**Cons**
- Metadata Overhead: Tracking usage order can consume additional memory.

- Performance Cost: For large caches, maintaining the access order may introduce computational overhead.

- Not Adaptive: Assumes past access patterns will predict future usage, which may not always hold true.

#### **Least frequently used (LFU)**
LFU evicts the item with the lowest access frequency. It assumes that items accessed less frequently in the past are less likely to be accessed in the future.

**Pros**
- Efficient for Predictable Patterns: Retains frequently accessed data, which is often more relevant.

- Highly Effective for Popular Data: Works well in scenarios with clear "hot" items.

**Cons**
- High Overhead: Requires additional memory to track frequency counts.

- Slower Updates: Tracking and updating frequency can slow down operations.

- Not Adaptive: May keep items that were frequently accessed in the past but are no longer relevant.

#### **First in first out (FIFO)**
FIFO evicts the item that was added first, regardless of how often it’s accessed.

#### **Most recently used (MRU)**
MRU is the opposite of Least Recently Used (LRU). In MRU, the item that was accessed most recently is the first to be evicted when the cache is full.

#### **Time to live (TTL)**
TTL is a cache eviction strategy where each cached item is assigned a fixed lifespan. Once an item’s lifespan expires, it is automatically removed from the cache, regardless of access patterns or frequency.

#### **✅ Problem statement**
Create a simple in-memory cache that supports:

- `get(key)`, `put(key, value, ttl)`  
- Least Recently Used (LRU) eviction
- Least Frequently Used (LFU) eviction
- Time-based expiration (TTL)  
- **Optional**: Auto-cleanup of expired keys

#### 💡 Mindset Shift
Focus on:

- Why does cache eviction policy matter for user experience or system performance?  
- Where would you place this cache — browser, edge, DB layer?

#### 📚 Learning Objective
Grasp how caching improves latency, scalability, and how eviction/expiration strategies affect system design.

