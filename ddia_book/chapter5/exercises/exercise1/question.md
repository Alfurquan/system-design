# 💡 Problem Statement

Build a small key-value store that simulates replication between a leader and one or more follower nodes. The system should:

- Allow writes to the **leader**.
- Replicate those writes to **followers**.
- Simulate **delays or failures** in replication.
- Support **reads** from both leader and followers to observe **consistency lags**.

---

# 🧠 Concepts Practiced

- Leader-based replication  
- Write-ahead log  
- Asynchronous vs. synchronous replication  
- Read-your-writes consistency  
- Fault tolerance and failover  
- Replication lag  

---

# 🛠️ Hints to Guide Implementation

### 1. Basic Structure

- **Leader node**: Accepts writes and sends updates to followers.  
- **Follower nodes**: Replicate data from the leader.

### 2. Write Log

- Maintain a **write-ahead log** (e.g., `[{ op: "set", key: "x", value: 1, ts: 1001 }]`) on the leader.
- Replicate log entries to followers.

### 3. Replication Strategy

- Start with **asynchronous replication** (send logs with delay).
- Add a toggle to simulate **synchronous replication** and compare behaviors.

### 4. Failure Simulation

- Introduce artificial **delays**, **dropped messages**, or **crashes** for followers.
- Demonstrate how followers fall behind and **recover** using logs.

### 5. Read Operations

- Implement:
  - **Strong reads** (from the leader)
  - **Potentially stale reads** (from a follower)
- Log timestamps to observe **replication lag** between leader and followers.

### 6. Client Session Support (Optional)

- Add basic **client session tracking** to simulate:
  - **Read-your-writes**
  - **Monotonic reads**

---

# 🚀 Bonus Extensions (Advanced)

- Implement **automatic failover**: Elect a new leader when the current one crashes.
- Use **version vectors** or **log sequence numbers (LSNs)** for consistency checks.
- Add **quorum reads/writes** (a segue into Chapter 9 of *Designing Data-Intensive Applications*).