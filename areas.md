# System Design Preparation

## 🔹 Database and Storage Fundamentals

- **ACID vs BASE** — Consistency, Isolation, Durability
- **Normalization vs Denormalization** — When and why
- **Indexing** — Clustered vs Non-Clustered, Composite Index
- **Primary, Foreign Keys, Constraints**
- **Transactions and Concurrent Operations**
- **Storage Types** — File storage, Blob, Block, Object storage
- **SQL vs NOSQL** - Trade offs
- **Types of NO SQL Dbs** - Trade offs and when to use what.
- **Replication and Sharding** — Horizontal vs Vertical
- **Backup and Restore Operations**
- **Time-series and Caching Stores** (Redis, Memcached)

---

## 🔹 Networking Fundamentals

- **OSI Model Layers and TCP/IP Stack**
- **DNS and CDNs** — Caching, routing
- **Load Balancing** — L4 vs L7, reverse proxy, health checks
- **API Gateways and Service Meshes**
- **Traffic Control** — Rate-limits, backpressure, congestion
- **Security Layers** — TLS, certificates, firewalls, DDoS mitigation
- **Content Delivery Networks (For media, static files)**

---

## 🔹 Scalability Fundamentals

- **Vertical vs Horizontal Scaling**
- **Partitioning and Sharding** — Hash sharding, range sharding, directory
- **Read/Write Split — Primary/Replica, Multi-region copies
- **Event-Driven and Pub/Sub Architectural Styles** (for high-throughput workloads)
- **CQRS (Command Query Responsibility Segregation) and Caching Layers**
- **Rate-limiting and Throttling**

---

## 🔹 API Fundamentals

- **REST vs RPC vs gRPC vs GraphQL** — Choosing the right style
- **API Versioning and Backward Compatibility**
- **Rate-Limits, Authentication, Authorization (RBAC, OAuth)**
- **API Gateway, API Security, API Throttling, API Caching**
- **Designing for Extensibility — pagination, filtering, expansion**

---

## 🔹 Capacity Estimation (Mastering)

- **Traffic estimates (RPS, QPS) and data sizes per request**
- **Storage estimates** (number of records, size per record)
- **Compute estimates** (CPU, RAM usage per request)
- **Disk I/O and Network usage estimates under load**
- **Scaling plans and capacity buffers (active-active, fallback clusters)**

---

## 🔹 Additional Topical Areas (Consider adding)

✅ **Event-Driven Architectural Patterns**  
- Pub/Sub, messaging queues (Amazon SQS, Apache Kafka)  
- Stream processing (Flink, Kafka Streams)

✅ **Cache Design**  
- Local vs distributed cache (Redis, Memcached)  
- Write-through vs write-around vs cache-aside strategies  
- Invalidation and expiration mechanisms

✅ **Consistency and Partition Tolerance**  
- CAP Theorem — eventual vs strong consistency  
- Multi-region data synchronization  
- Quorum mechanisms (Read repair, conflict resolution)

✅ **Security and Authentication**  
- OAuth, SAML, JWT  
- Multi-factor Authentication (MFA)  
- Role-Based Access Control (RBAC) vs Attribute-Based (ABAC)  
- Security audits and vulnerability scanning  

✅ **Rate-limiting and Throttling**  
- Token Bucket, Leaky Bucket, Fixed Window, Sliding Window  
- Global vs per-user rate-limits  
- Implementing backpressure gracefully  

✅ **Audit, Observability and Operations**  
- Logs, Metrics, Trace IDs
- Dashboards (Grafana), alert mechanisms (Prometheus alerts)
- SLOs, SLAs, Error Budgets
- Chaos testing and resiliency practices

---