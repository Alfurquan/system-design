# What is a distributed cache and when should you use it?

In most system design interviews you'll be tasked with both scaling your system and lowering system latency. One common way to do this is to use a distributed cache. A cache is just a server, or cluster of servers, that stores data in memory. They're great for storing data that's expensive to compute or retrieve from a database.

## Use cases

- **Save Aggregated Metrics:** Consider an analytics platform that aggregates data from numerous sources to display a dashboard of metrics. The data for these metrics is expensive to compute, so the platform calculates metrics asynchronously (like hourly via a background job) and stores the results in a distributed cache. When a user requests a dashboard, the platform can retrieve the data from the cache instead of recomputing it, reducing latency.

- **Reduce Number of DB Queries:** In a web application, user sessions are often stored in a distributed cache to reduce the load on the database. This is especially important for systems that need to support a large number of concurrent users. When a user logs in, the system can store their session data in the cache, allowing the system to quickly retrieve the data when the user makes a request.

- **Speed Up Expensive Queries:** Some complex queries take a long time to run on a traditional, disk based database. For example, if you have a social media platform like Twitter, you might want to show users a list of posts from people they follow. This is a complex query that requires joining multiple tables and filtering by multiple columns. Running this query on Postgres could take ages. Instead, you can run the query once, store the results in a distributed cache, and then retrieve the results from the cache when a user requests them.

## Things you should know about distributed caches for your interview

- **Eviction Policy:** Distributed caches have different eviction policies that determine which items are removed from the cache when the cache is full. Some common eviction policies are:
    - **Least Recently Used (LRU):** Evicts the least recently accessed items first.
    - **First In, First Out (FIFO):** Evicts items in the order they were added.
    - **Least Frequently Used (LFU):** Removes items that are least frequently accessed.

- **Cache Invalidation Strategy:** This is the strategy you'll use to ensure that the data in your cache is up to date. For example, if you are designing Ticketmaster and caching popular events, then you'll need to invalidate an event in the cache if the event in your Database was updated (like the venue changed).

- **Cache Write Strategy:** This is the strategy you use to make sure that data is written to your cache in a consistent way. Some strategies are:

- **Write-Through Cache:** Writes data to both the cache and the underlying datastore simultaneously. Ensures consistency but can be slower for write operations.

- **Write-Around Cache:** Writes data directly to the datastore, bypassing the cache. This can minimize cache pollution but might increase data fetch times on subsequent reads.

- **Write-Back Cache:** Writes data to the cache and then asynchronously writes the data to the datastore. This can be faster for write operations but can lead to data loss if the cache is not persisted to disk.