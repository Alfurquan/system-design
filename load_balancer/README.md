## What is a load balancer ?
A load balancer is a system that spreads incoming network traffic across multiple backend servers.

## Why we need it ?

- Scalability: As traffic grows, we can add more servers behind the load balancer without redesigning our entire architecture.
- High availability: If one server goes offline or crashes, the load balancer automatically reroutes traffic to other healthy servers.
- Performance optimization: Balancing load prevents certain servers from overworking while others remain underutilized.
- Maintainability: We can perform maintenance on individual servers without taking our entire application down.

## How load balancing works ?

- Traffic Reception: All incoming requests arrive at the load balancer’s public IP or domain.

- Decision Logic (Routing Algorithm): The load balancer decides which server should get the request. Common routing algorithms include:
    - Round Robin: Requests are distributed sequentially to each server in a loop.
    - Weighted Round Robin: Each server is assigned a weight (priority). Servers with higher weights receive proportionally more requests.
    - Least Connections: The request goes to the server with the fewest active connections.
    - IP Hash: The load balancer uses a hash of the client’s IP to always route them to the same server (useful for sticky sessions).
    - Random: Select a server randomly (sometimes used for quick prototypes or specialized cases).

- Server Health Checks: Load balancers usually have an internal mechanism to periodically check if servers are alive (e.g., by sending a heartbeat request like an HTTP GET /health).

    - If a server doesn’t respond within a certain threshold, it’s marked as unhealthy and no longer receives traffic.
    - When it recovers, the load balancer can automatically reintroduce it into the rotation.

- Response Handling: Once a request is forwarded to a healthy server, the server processes it and returns the response to the load balancer, which then returns it to the client.

## Consistent hashing
Consistent hashing is a distributed hashing technique used to efficiently distribute data across multiple nodes (servers, caches, etc.).
It uses a circular hash space (hash ring) with a large and constant hash space.

In consistent hashing, when the number of nodes changes, only k/n keys need to be reassigned, where k is the total number of keys and n is the total number of nodes.

### ✅ Problem Statement
Design and implement a simulation of a load balancer that distributes incoming HTTP requests across a pool of backend servers. Your balancer should support:

- Round-robin routing  
- Random selection
- Weighted round robin
- Least connections
- IP Hash
- Consistent hashing  
- Simulate backends going offline and recovering  
- **Bonus**: Implement active health checks for servers

### 💡 Mindset Shift
Instead of just implementing, ask:

- Why does consistent hashing reduce rebalancing?  
- When should you use client-side load balancing vs a centralized gateway like Envoy?

### 📚 Learning Objective
Understand traffic distribution strategies, fault tolerance, and how load balancers affect system resilience.