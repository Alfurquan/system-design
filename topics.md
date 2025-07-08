# 📘 System Design Interview Prep — Focus Topics (Google & Top Tech Companies)

## 📚 Core Topics to Master

### 1. Storage Fundamentals
- Relational (SQL) vs Document (NoSQL) vs Key-Value stores
- ACID vs BASE trade-offs
- How to choose the right storage based on:
  - Access patterns (read-heavy, write-heavy, etc.)
  - Consistency, latency, and scalability requirements

### 2. Scalability Concepts
- Vertical vs Horizontal Scaling
- Read/Write segregation strategies
- Partitioning/Sharding techniques
  - Static vs Dynamic Sharding
  - Challenges (rebalancing, joins, hotspots)
- Hotspot/Celebrity problem solutions
- Load Balancing Algorithms:
  - Round-robin
  - Least-connections
  - Consistent Hashing

### 3. Networking & Communication
- TCP vs UDP
- HTTP/HTTPS lifecycle
- DNS resolution
- REST vs GraphQL vs gRPC
- Real-time communication:
  - WebSockets
  - Server-Sent Events (SSE)

### 4. Performance & Capacity Planning
- Latency benchmarks for:
  - Memory access
  - Disk I/O
  - Network requests
- Throughput calculations (QPS, IOPS)
- Basic capacity planning techniques
- Performance bottlenecks and solutions:
  - Caching (read/write)
  - Indexing
  - Sharding writes

### 5. Fault Tolerance & Redundancy
- Replication strategies:
  - Leader-follower
  - Multi-leader
  - Quorum-based
- Failure detection mechanisms:
  - Heartbeats
  - Timeouts
- Designing for redundancy:
  - Server, rack, and data center level
- Graceful degradation, retries, fallback strategies

### 6. CAP Theorem
- Understand the trade-offs:
  - Consistency
  - Availability
  - Partition Tolerance (always assumed)
- Classify systems as CP, AP, or CA
- Use-case driven consistency decisions:
  - Strong consistency: Banking, bookings
  - Eventual consistency: Social feeds, analytics

---

## 🧱 System Design Building Blocks

Know the **purpose**, **pros/cons**, and **failure modes** for each:

| Component         | Purpose & Key Points |
|------------------|----------------------|
| **Server/Compute** | Executes business logic (Monolith, Microservices, Serverless) |
| **Database**       | Persistent structured data (RDBMS, Document, Key-Value, Column) |
| **Cache**          | Low-latency reads (Redis, Memcached); Patterns: Cache-aside, Read-through, Write-through |
| **Message Queue**  | Asynchronous workflows & backpressure handling (Kafka, RabbitMQ, SQS) |
| **Load Balancer**  | Distributes load across servers; Algorithms: Round-robin, Least-connections, Consistent Hashing |
| **Blob Storage**   | Unstructured data storage (S3, GCS); Lifecycle policies |
| **CDN**            | Caches static content near the user; Reduces latency, protects origin |

---

## 🔍 Bonus Areas to Explore
- High Availability (HA) & Disaster Recovery (DR)
- Rate Limiting & Throttling
- Security: Authentication, Authorization, API rate limits
- Observability:
  - Logging
  - Metrics
  - Tracing (e.g. OpenTelemetry)
- API Versioning & Backward Compatibility

---

*Practice building systems using these concepts and components. Think through trade-offs and draw component diagrams to explain your choices.*
