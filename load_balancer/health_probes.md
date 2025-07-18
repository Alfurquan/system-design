# 🫀 HEALTH CHECKS (Probes)

## 🎯 Goal

Ensure the load balancer only routes traffic to healthy backend servers.

## ✅ Types of Health Checks

### Active Probes (LB → Backend)

The load balancer periodically sends requests to each server to check its health.

**Protocols used:**

- TCP probe: Open TCP connection (e.g., port 80/443)
- HTTP probe: Send HTTP GET /health (most common)
- Custom probe: Hit a business-critical endpoint and verify logic

**Pros:**

- Direct and controlled
- Doesn't rely on backend self-reporting
- Can simulate real-world behavior

**Cons:**

- Adds extra network load
- Must tune frequency to avoid false positives
  
### Passive probes (LB watches live traffic)

The load balancer observes real user traffic:

- 5xx responses
- Timeouts
- Connection resets

**Pros:**

- No extra traffic
- Reflects actual user experience

**Cons:**

- Only catches issues after bad user experience
- May take longer to detect issues

### Heartbeat (Server → LB)

Backend server pushes health signals (e.g., heartbeat pings) to LB.

**Pros:**

- Backend has richer context (CPU, memory, etc.)
- Push-based: can be more immediate

**Cons:**

- Backend needs extra logic
- Trust issues: faulty server may still send heartbeat
- At scale, LBs may get overwhelmed by heartbeats.

### ⚙️ Best Practices

- Use combination of active and passive health checks.
- Introduce grace periods and hysteresis:
  - E.g., mark a server unhealthy only after 3 consecutive failures.
  - Wait 1–2 successful checks before marking a server healthy again.

- Set thresholds carefully based on system SLA.

- Support customizable health endpoints on each service.

--- 

# 🔁 FAILOVER BETWEEN LOAD BALANCERS

## 🎯 Goal

If the primary load balancer fails, another load balancer should take over seamlessly — without user impact.

## 🔑 Key Challenges

- Detecting when the primary LB has failed.
- Promoting the secondary LB.
- Ensuring only one is active (avoid split brain).
- Making the client redirect or reconnect gracefully.

## 🧩 Common Approaches

### 1. Virtual IP (VIP) + Failover Control

Use a shared virtual IP address that only one load balancer (LB) can bind to at a time.

A control mechanism decides who owns the VIP (usually via heartbeat).

If the primary fails, the standby LB takes over the VIP.

**Examples:** `Keepalived`, `VRRP protocol`

**Pros:**

- Transparent to clients  
- Very fast failover (~subsecond)

**Cons:**

- Limited to Layer 2 networks  
- Harder to scale globally

---

### 2. DNS Failover

Domain (e.g., `lb.example.com`) resolves to multiple LBs.

If the primary fails, health-aware DNS updates the record to point to the standby LB.

**Pros:**

- Simple  
- No VIP constraints

**Cons:**

- DNS TTL caching causes slow failover (minutes)  
- Can’t guarantee clients pick new address quickly

---

### 3. Distributed Coordination (Consensus)

Use a system like `etcd`, `Zookeeper`, or `Consul` for:

- Leader election  
- Heartbeat tracking  
- Failover decision-making

LBs periodically check into a central store.  
Only the leader serves traffic; others are on standby.

**Pros:**

- Works across data centers or cloud zones  
- Scalable and observable

**Cons:**

- Adds infrastructure complexity  
- Slight delay in failover (~seconds)

---

## ⚖️ Split-Brain Protection

To ensure only one LB is active at a time:

- Use lock mechanisms (e.g., distributed locks)  
- Let only the leader own the VIP or serve DNS records  
- Use watchdog processes to detect conflicts and demote nodes

---

## 📈 Metrics to Track

- LB uptime and role status (primary/standby)  
- Number of backend failures  
- Time to failover  
- Traffic drop rate during failover

---

## 🔐 Bonus (Security)

- Use TLS between LB and backend  
- Protect health check endpoints from the public  
- Use mutual TLS for heartbeat authenticity