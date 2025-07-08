## What is a rate limiter ?

In a network system, a rate limiter is used to control the rate of traffic sent by a client or a service. In the HTTP world, a rate limiter limits the number of client requests allowed to be sent over a specified period. If the API request count exceeds the threshold defined by the rate limiter, all the excess calls are blocked. Here are a few examples:

- A user can write no more than 2 posts per second.
- You can create a maximum of 10 accounts per day from the same IP address.
- You can claim rewards no more than 5 times per week from the same device.

## Algorithms for rate limiting

### Token bucket

The token bucket algorithm is widely used for rate limiting. It is simple, well understood and commonly used by internet companies. 

**How it works?**

- Imagine a bucket that holds tokens.
- The bucket has a maximum capacity of tokens.
- Tokens are added to the bucket at a fixed rate (e.g., 10 tokens per second).
- When a request arrives, it must obtain a token from the bucket to proceed.
- If there are enough tokens, the request is allowed and tokens are removed.
- If there aren't enough tokens, the request is dropped.

The token bucket algorithm takes two parameters:

- Bucket size: the maximum number of tokens allowed in the bucket
- Refill rate: number of tokens put into the bucket every second

**Pros**

- The algorithm is easy to implement.
- Memory efficient.
- Token bucket allows a burst of traffic for short periods. A request can go through as long as there are tokens left.

**Cons**
Two parameters in the algorithm are bucket size and token refill rate. However, it might be challenging to tune them properly.

### Leaky bucket
The leaking bucket algorithm is similar to the token bucket except that requests are processed at a fixed rate. It is usually implemented with a first-in-first-out (FIFO) queue. The algorithm works as follows:

- When a request arrives, the system checks if the queue is full. If it is not full, the request is added to the queue.
- Otherwise, the request is dropped.
- Requests are pulled from the queue and processed at regular intervals.

Leaking bucket algorithm takes the following two parameters:

- Bucket size: it is equal to the queue size. The queue holds the requests to be processed at a fixed rate.
- Outflow rate: it defines how many requests can be processed at a fixed rate, usually in seconds.

**Pros**

- Memory efficient given the limited queue size.
- Requests are processed at a fixed rate therefore it is suitable for use cases that a stable outflow rate is needed.

**Cons**

- A burst of traffic fills up the queue with old requests, and if they are not processed in time, recent requests will be rate limited.
- There are two parameters in the algorithm. It might not be easy to tune them properly.

### Fixed window counter

Fixed window counter algorithm works as follows:

- The algorithm divides the timeline into fix-sized time windows and assign a counter for each window.
- Each request increments the counter by one.
- Once the counter reaches the pre-defined threshold, new requests are dropped until a new time window starts.

**Pros**
- Easy to implement and understand.
- Provides clear and easy-to-understand rate limits for each time window.

**Cons**
- Does not handle bursts of requests at the boundary of windows well. Can allow twice the rate of requests at the edges of windows.

### Sliding window log
The Sliding Window Log algorithm keeps a log of timestamps for each request and uses this to determine if a new request should be allowed.

**How it works**
- Keep a log of request timestamps.
- When a new request comes in, remove all entries older than the window size.
- Count the remaining entries.
- If the count is less than the limit, allow the request and add its timestamp to the log.
- If the count exceeds the limit, request is denied.

**Pros**
Rate limiting implemented by this algorithm is very accurate. In any rolling window, requests will not exceed the rate limit.

**Cons**
The algorithm consumes a lot of memory because even if a request is rejected, its timestamp might still be stored in memory.

### Sliding window counter
The sliding window counter algorithm is a hybrid approach that combines the fixed window counter and sliding window log. 

Instead of keeping track of every single request’s timestamp as the sliding log does, it focus on the number of requests from the last window.

So, if you are in 75% of the current window, 25% of the weight would come from the previous window, and the rest from the current one:

`weight = (100 - 75)% * lastWindowRequests + currentWindowRequests`

**How it works**
- Keep track of request count for the current and previous window.

- Calculate the weighted sum of requests based on the overlap with the sliding window.

- If the weighted sum is less than the limit, allow the request.


**Pros**
- More accurate than Fixed Window Counter.
- More memory-efficient than Sliding Window Log.
- Smooths out edges between windows.

**Cons**
Slightly more complex to implement.

## Rate Limiting Algorithms: Comparison & When to Use What

### ✅ Overview of Algorithms

| Feature / Algorithm         | Fixed Window            | Sliding Window Log         | Sliding Window Counter      | Leaky Bucket                | Token Bucket                |
|----------------------------|--------------------------|-----------------------------|------------------------------|-----------------------------|-----------------------------|
| **Burst Handling**         | ❌ No (strict cutoff)     | ✅ Yes (fine-grained logs)   | ⚠️ Limited (stepwise bursts)  | ❌ No                       | ✅ Yes                      |
| **Request Smoothing**      | ❌ No                     | ✅ Yes                       | ✅ Yes                        | ✅ Yes                      | ❌ Not inherently           |
| **Memory Usage**           | 🟢 Low                    | 🔴 High (per-request log)    | 🟡 Medium                     | 🟡 Medium                   | 🟡 Medium                   |
| **Implementation Ease**    | 🟢 Very Easy              | 🔴 Complex (log maintenance) | 🟡 Moderate                   | 🟢 Simple                   | 🟡 Moderate                 |
| **Time Precision**         | ❌ Coarse (per interval)  | ✅ Precise                   | ⚠️ Less precise               | ✅ Good                     | ✅ Good                     |
| **Throttling Style**       | Hard limit               | Hard limit                  | Hard limit                   | Drip-out (uniform flow)    | Credit-based (bursty flow) |
| **Best For**               | Simple APIs, low-scale   | Security, fine limits       | High-traffic APIs            | Outgoing shaping            | Burst-tolerant services     |

---

### ✅ When to Use What — Real-World Scenarios

| Scenario                                     | Recommended Algorithm           | Why                                                         |
|---------------------------------------------|----------------------------------|-------------------------------------------------------------|
| 🔐 Login/Signup Brute-force Protection       | **Leaky Bucket**                | Prevents floods, smooth traffic                            |
| 🚀 Burst Traffic Allowed                     | **Token Bucket**                | Supports burst, enforces average rate                      |
| 📊 Precise Request Tracking                  | **Sliding Window Log**          | High accuracy with actual timestamps                       |
| 🔄 Simple API Quotas                         | **Fixed Window**                | Simple to implement, low overhead                          |
| 📈 Large-scale APIs with smoothing           | **Sliding Window Counter**      | Good accuracy/performance balance                          |
| 🌐 CDN / API Gateway                         | **Leaky Bucket**                | Smooths traffic to downstream systems                      |
| 👥 Multi-tenant SaaS Rate Limiting           | **Token Bucket / Sliding Counter** | Good balance between fairness and flexibility         |
| 🧪 Dynamic/Experiment Traffic Controls       | **Token Bucket**                | Supports dynamic burst and throttle configs                |
| 🎮 Real-time Messaging Fairness              | **Leaky Bucket**                | Enforces uniform message flow                              |

---

### ✅ Quick Decision Table

| Goal                                         | Use This                         |
|---------------------------------------------|----------------------------------|
| Enforce **hard caps**                       | Fixed or Sliding Window          |
| Allow **bursts**                            | Token Bucket                     |
| **Smooth** request flow                     | Leaky Bucket                     |
| Have **precise logs**                       | Sliding Window Log               |
| Prioritize **simplicity**                   | Fixed Window or Token Bucket     |
| Avoid **excess memory** in large systems    | Token or Leaky Bucket            |

---

### ✅ Summary (Cheat Sheet)

- **Fixed Window** – Best for simple rate limits. ❌ Bursts at window edges.
- **Sliding Window Log** – Best accuracy, worst memory.
- **Sliding Window Counter** – Balanced accuracy & cost.
- **Leaky Bucket** – Smooth output, no bursts allowed.
- **Token Bucket** – Allows bursts, controls average rate.

---

