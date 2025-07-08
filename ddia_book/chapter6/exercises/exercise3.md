# 🐦 Exercise 3: Twitter-Like Feed Generation System

## 📘 Problem Statement

You're building a distributed system that supports timeline generation for a Twitter-like social media app.

### Requirements:

- Users can follow other users  
- When a user posts a tweet, it appears in the timeline of all their followers  
- Timeline view shows the most recent posts from followed users  

### System Load Characteristics:

- Most users have a few hundred followers  
- Some users (e.g., celebrities) have millions of followers (**hot users**)  
- Users open the app frequently to view their timeline (**read-heavy**)  
- Tweets are small (< 1KB) but arrive frequently (**write-heavy** for hot users)  
- System must **scale**, **minimize latency**, and **avoid hotspots**

---

## 🎯 Design Task

Focus on the partitioning strategy and answer the following:

### 🧠 What are the write and read access patterns?

### 🧩 What partitioning strategy would you use? Why?

### 🧯 How would you handle hot users with millions of followers?

### ⏳ How would you support efficient timeline reads per user?

---

## Solution

### 🧠 What are the write and read access patterns?

The system has a write pattern where tweeting may result in N writes (to N followers' timelines) — this is known as fan-out on write. Timeline views involve reading the most recent tweets from followed users — potentially 100s of reads per user action — which we call fan-out on read. The balance between these determines whether we push or pull feeds.

The system has a read access pattern when someone opens their app or goes to someone else's profile. Timeline views involve reading the most recent tweets from followed users — potentially 100s of reads per user action — which we call fan-out on read.

### 🧩 What partitioning strategy would you use? Why?

We can use hash based partitioning strategy here. We can first go with hash of userId to determine which partition the user's data goes to. Hashing will distribute the load across the nodes resulting in efficient and parallel querying of data. 

For hot keys, we’ll use key salting with multiple ‘virtual keys’ (e.g., user123_0, user123_1, etc.). Writes are sharded randomly across them. Reads use a fan-out read across all salted variants and aggregate results. We can track mapping of hot keys using a control structure or predefine the hot set.

### 🧯 How would you handle hot users with millions of followers?

For hot users, we’ll use key salting with multiple ‘virtual keys’ (e.g., user123_0, user123_1, etc.). Writes are sharded randomly across them. Reads use a fan-out read across all salted variants and aggregate results. We can track mapping of hot keys using a control structure or predefine the hot set.

### ⏳ How would you support efficient timeline reads per user?

Timeline views involve reading the most recent tweets from followed users — potentially 100s of reads per user action — which we call fan-out on read. We can use caching to cache data from hot users to allow efficient retrieval. Since all users data is partitioned across different nodes, we need to send request to all nodes and then aggregate the results back. So caching can help reduce the request to backend and help in boosting retrieval times.

---

## Improvements

### 🧩 What partitioning strategy would you use? Why?

⚠️ Room for Improvement:

You could’ve discussed how tweet data vs timeline feed data may be stored in separate partitioned stores:

- Tweets table → partitioned by author userId

- Timelines table → partitioned by consumer userId

Hashing works well for tweet inserts, but for timeline reads, you need efficient fan-in.

🧠 Suggestion:

“Tweets are partitioned by author ID (write-optimized). Timeline storage is partitioned by consumer ID — this allows efficient reads for getTimeline(user). Each write may result in N inserts into different consumer timeline partitions.”

### 🧯 How would you handle hot users with millions of followers?

⚠️ Missed Opportunity:

Salting the tweet key helps only somewhat. When a hot user tweets, the real problem is the fan-out to millions of followers.

The bottleneck isn’t writing the tweet — it’s writing that tweet to all those timelines, possibly across many partitions.

🧠 Stronger Answer:

“For hot users with millions of followers, we delay the fan-out and store the tweet in an author-based store. Timeline reads then pull tweets from those hot users in real-time (‘fan-out on read’), possibly with caching or precomputed batches for efficiency.”

This hybrid model (fan-out on write for normal users, fan-out on read for hot users) is used by real Twitter, Instagram, etc.

### ⏳ How would you support efficient timeline reads per user?

🧠 Suggestion:

“We precompute timelines for most users by maintaining an inbox table (partitioned by userId). When they open the app, we read from that inbox — already sorted and paginated. For hot users, we rely on caching and possibly compute timelines on read.”






