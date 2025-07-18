# Health Checks and heartbeats

Notes on health checks and heart beat protocols in system design

## Health check end point

A microservice's health check or heartbeat endpoint (e.g. GET /v1/health) exists to let a requester know if the service instance is healthy or not. The response is typically an HTTP 200 (healthy) or non-200 (unhealthy) status.

We can define healthy as:

- The instance has started
- The instance has a live connection to its data stores (including message brokers)
- The instance is actively processing (serving requests, consuming messages, etc.)
- The instance has enough required resources (heap memory, disk space, etc.)

Service orchestrators and monitors periodically make requests to this endpoint to know whether a service instance is healthy, and if it is not then the orchestrator can take some kind of action (e.g. kill the instance and start a new one).

Polling a health check endpoint is a form of black box monitoring where the requester has no visibility into the internals of the service, it only knows if it received a success or error response.

### What a health check shouldn't include ?

- Internal dependent services.

Let's say you have a service currency-api that some large number of microservices in your ecosystem depend on. If currency-api starts failing, and all services that depend on it query currency-api in their health check, then you will have a cascading effect where all of those services will become unhealthy as well. A better pattern may be to keep a cache of the last known successful response, depending on your business requirements.

- External (SaaS) dependent services.

If your service relies on a vendor and cannot use stale data, such as an identity provider, then your service should remain healthy and respond with an appropriate error status. In this scenario, there is nothing operably wrong with your service, it is performing as expected, so it remains healthy. You may still want to alert the owning team about the issue, however.

### Anatomy of a health check response

Most of the time a simple HTTP 200 or non-200 status is enough for a health check response. You could consider adding additional detail in the response so a human can gain more insight, but it might be just as effective to emit this information in logs or metrics.

Here's an example response you could use:

```json
{
  "status": "UP",
  "uptime": 74.766,
  "checks": {
    "kafka": "UP",
    "postgresql": "UP",
    "heapSpaceFree": "88M"
  }
}
```

### Health checks in load balancers

Health checks are automated processes that monitor the status of backend servers in a load-balanced environment. They ensure that traffic is only sent to servers that are up and running smoothly. Think of them as the load balancer's eyes and ears, constantly checking to see if everything is okay.

### Why Are Health Checks Important?

Imagine you're running an e-commerce site. During a big sale, traffic spikes, and suddenly, one of your servers goes down. Without health checks, the load balancer would keep sending traffic to that dead server, leading to dropped requests and unhappy customers. Health checks prevent this by quickly identifying and isolating unhealthy servers, ensuring that traffic is only sent to healthy ones.

### Types of Health Checks

Health checks come in various flavors, each suited to different types of applications and infrastructure. The most common types are:

- **HTTP/HTTPS Checks:** These checks send an HTTP or HTTPS request to a specified path on the server and expect a successful response (usually a 200 OK status code).

- **TCP Checks:** These checks establish a TCP connection to a specified port on the server. If the connection is successful, the server is considered healthy.

- **ICMP Checks:** These checks send ICMP (ping) requests to the server and expect a response. This is a simple way to check if the server is reachable.

- **Custom Checks:** These are more complex and can involve custom scripts or commands that run on the server to check its health.

### Key Components of a Health Check

A health check typically consists of several key components:

- **Interval:** How often the health check is performed.
- **Timeout:** How long the load balancer waits for a response before considering the check failed.
- **Threshold:** The number of consecutive successful or failed checks required to change the server's health status.
- **Path:** The specific endpoint or resource that the health check targets.

### Configuring Health Checks

Configuring health checks involves setting these components to values that make sense for your application. For example, if you're running a high-traffic website, you might want to perform health checks every 10 seconds with a timeout of 5 seconds. If you're running a less critical application, you might perform checks every minute with a longer timeout.

### Best Practices for Health Checks

Setting up health checks is just the first step. To ensure they're effective, you need to follow some best practices:

- **Use Application-Specific Endpoints:** Instead of checking the root path, use an endpoint that specifically checks the health of your application.

- **Monitor Critical Dependencies:** Ensure that your health checks also monitor critical dependencies like databases or external services.

- **Set Appropriate Thresholds:** Don't set your thresholds too low or too high. Too low, and you risk false positives; too high, and you might miss genuine issues.

- **Regularly Review and Update:** Health checks aren't a set-it-and-forget-it thing. Regularly review and update them to ensure they're still effective.

### Common Pitfalls to Avoid

Even with the best intentions, there are some common pitfalls to avoid when setting up health checks:

- **Overly Aggressive Checks:** Checking too frequently or with too short a timeout can overwhelm your servers.

- **Ignoring Dependencies:** Focusing only on the server itself and ignoring critical dependencies can lead to false positives.

- **Inadequate Monitoring:** Relying solely on health checks without additional monitoring can leave you blind to other issues.

---

## Heartbeats

Heartbeat messages are periodic signals sent between components of a distributed system to indicate that they are still alive and functioning properly. These messages serve as a form of health check, allowing each component to monitor the status of its peers and detect failures or network issues. The term "heartbeat" comes from the analogy of the periodic pulsing of a heart, indicating that it is still beating and functioning. Similarly, in a distributed system, heartbeat messages are regularly sent between components to ensure that they are operational.

### Importance of Heartbeat Messages in Distributed Systems

- **Failure Detection:** Heartbeat messages are used to detect failures in distributed systems. By regularly sending and monitoring heartbeat messages, components can quickly detect when a peer becomes unresponsive or fails. This allows for timely action to be taken, such as initiating failover procedures or restarting the failed component.

- **Health Monitoring:** Heartbeat messages provide a way to monitor the health and availability of components in real time. By analyzing the receipt of heartbeat messages, administrators can gain insights into the overall health of the system and identify potential issues before they cause major problems.

- **Load Balancing:** In systems where components are responsible for handling incoming requests or tasks, heartbeat messages can be used for load balancing. By monitoring the load and availability of components through heartbeat messages, requests can be routed to the most suitable and available components, ensuring optimal performance and resource utilization.

- **Network Partition Detection:** Heartbeat messages can also be used to detect network partitions, where components become isolated from each other due to network issues. By monitoring the receipt of heartbeat messages, components can detect when they are no longer receiving messages from certain peers, indicating a potential network partition.

- **Maintaining Consistency:** In systems that use distributed consensus algorithms, such as Paxos or Raft, heartbeat messages are used to maintain consistency among nodes. These algorithms rely on regular communication between nodes, and heartbeat messages ensure that nodes are still reachable and operational.

### Components of Heartbeat Messages

Heartbeat messages in a distributed system usually contain multiple components that communicate critical information about the identity, health, and status of the sender.

**1. Identification:**

- Sequence Number: In order to assist recipients in tracking the sequence of messages received and identifying any missed or out-of-order messages, certain heartbeat messages contain a sequence number or sequence ID. Sequence numbers help to identify possible communication problems or message loss and enable dependable message delivery.

- Node/Component Identifier: An identifier, also known as a unique identifier (ID), is usually included in each heartbeat message to identify the sender node or component in the distributed system. With the aid of this identifier, recipients are able to identify the source of the heartbeat message and link it to the appropriate node or component.

**2. Liveness Signal:**

- Timestamp: A timestamp that shows the message's send time is frequently included in heartbeat messages. This timestamp helps in evaluating the message's freshness and enables recipients to determine when the sender last communicated.

**3. Optional Additional Information (Depending on Implementation):**

- Payload/Data: Additional payload or information about the health or status of the sender may be included in heartbeat messages. Version numbers, configuration details, and other relevant information that receivers require to evaluate the sender's status or condition may be included in this payload.
  
- Acknowledgment (ACK):Heartbeat messages occasionally have an acknowledgment (ACK) mechanism that allows the recipient to verify that they have received the message. By verifying that the message was successfully received and processed by the recipient, this ACK provides feedback to the sender.

- Timeout/Expiration Information: Information regarding message expiration or timeout thresholds may also be included in heartbeat messages. When a message delivery exceeds a specific limit, this information aids recipients in verifying the message's validity and applying timeout handling mechanisms.

**4. Minimal Overhead**

- Status Information: The sender node or component's current operational status, health, or state may be indicated by status information included in heartbeat messages. Metrics like CPU and memory usage, disk space availability, network connectivity, and any other appropriate health indicators could be included in this data.

**5. Security Considerations**

- Checksum/Hash: Heartbeat messages may contain a checksum or hash value computed based on the message content in order to guarantee message integrity and identify tampering or corruption. This checksum can be used by recipients to confirm the message's integrity and identify any unauthorized changes.

### Heartbeat Protocols

In distributed systems, heartbeat protocols are used as a means of communication to transfer heartbeat messages amongst nodes or components.

**Simple Heartbeat Protocol (SHP)**

SHP uses a straightforward message exchange to report the availability and liveness of nodes at regular intervals.

**Ping/Echo Protocol**

Sending a "ping" message from one node to another and waiting for a "echo" response from the receiving node is the Ping/Echo protocol, also called the Ping-Pong protocol.

**TCP-based Heartbeat Protocol**

In these protocols, nodes create a TCP connection and communicate by sending each other heartbeat messages over the connection.

**Raft Protocol**

- A consensus protocol called Raft is used in distributed systems to accomplish replication and fault tolerance.
- Heartbeat messages are used by the Raft protocol in the leader election and replication procedures.
- In a distributed system based on Raft, nodes communicate via heartbeat messages to track the health of the leader and identify any malfunctions.
