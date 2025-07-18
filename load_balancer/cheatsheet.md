# 🧾 Load Balancer Design – L5 SWE Cheatsheet

## 🎯 Goals
- Distribute traffic to backend servers efficiently.
- Handle failures gracefully (backend or LB).
- Ensure high availability and low latency.
- Support optional features like stickiness, SSL, observability.

## 🧱 Core Components
- **Load Balancer (LB)**: Entry point for all client traffic.
- **Backend Pool**: Servers handling business logic.
- **Health Checker**: Ensures only healthy backends serve traffic.
- **Sticky Session Logic** *(optional)*.
- **Failover Mechanism**: Secondary LB if primary fails.
- **SSL Termination** *(optional)*.

## ⚖️ Load Balancing Algorithms

| Strategy         | Stateless | Stickiness | Notes                          |
|------------------|-----------|------------|--------------------------------|
| Round Robin      | ✅        | ❌         | Simple, fair, not sticky       |
| Least Connections| ❌        | ⚠️         | Tracks live connection counts  |
| IP Hash          | ✅        | ✅         | Fragile with NATs, DHCP        |
| Cookie-Based     | ✅        | ✅         | Best for web apps              |
| Affinity Table   | ❌        | ✅         | Needs shared state (e.g. Redis)|

## 🫀 Health Checks

| Type     | Description                       | Example                     |
|----------|-----------------------------------|-----------------------------|
| Active   | LB → `/health` on each backend    | HTTP/TCP probe              |
| Passive  | Observe real traffic for failures | Timeouts, 5xx, resets       |
| Heartbeat| Backend → LB (push model)         | Pings, status metrics       |

✅ Combine active + passive.  
✅ Use hysteresis (N fails to mark down, M passes to mark up).

## 🔁 Failover Between LBs

**Approaches:**
- **VIP + Heartbeat**: Only active binds to shared IP.
- **DNS Failover**: Update DNS on failure (slow, cached).
- **Consensus/Leader Election**: Use etcd/Zookeeper/Consul.

**Split-brain prevention:**
- Only one LB owns VIP or lock.
- Secondary only takes over after timeout.

## 🧷 Session Stickiness

**Methods:**
- IP Hash: quick but brittle.
- Cookie-Based: LB injects cookie → consistent routing.
- Redis-Based Affinity Map: session ID → backend.

**Tips:**
- Add TTL to Redis keys.
- Redis must be HA.
- Plan for rebalancing if backend is removed.

## 🔒 SSL Termination

- **Terminate at LB** to simplify backend.
- Use **Let's Encrypt** or **Certificate Manager**.
- Store certs securely (Vault, KMS, encrypted disk).
- Rotate certs automatically.
- If needed, support **SSL passthrough** for compliance.

## 📊 Observability (Bonus)

- Emit metrics: QPS, backend error rates, LB CPU/mem.
- Log health check failures, reassignment events.
- Use dashboards & alerts (e.g., Prometheus + Grafana).

## 💬 Interview Tips

- Start with **goals** and **traffic flow**.
- Layer in features **one at a time**.
- Think about **scaling pain points**.
- Always mention **tradeoffs**.