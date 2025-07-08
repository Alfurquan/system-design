# Networking

## Networking 101

At its core, networking is about connecting devices and enabling them to communicate. Networks are built on a layered architecture (the so-called "OSI model") which greatly simplifies the world for us application developers who sit on top of it.

## Networking layers

Three important layers

### Network layer

At this layer is IP, the protocol that handles routing and addressing. It's responsible for breaking the data into packets, handling packet forwarding between networks, and providing best-effort delivery to any destination IP address on the network. While there are other protocols at this layer (like InfiniBand, which is used extensively for massive ML training workloads), IP by far the most common for system design interviews.

### Transport layer

At this layer, we have TCP, QUIC, and UDP, which provide end-to-end communication services. Think of them like a layer that provides features like reliability, ordering, and flow control on top of the network layer.

### Application layer

At the final layer are the application protocols like DNS, HTTP, Websockets, WebRTC. These are common protocols that build on top of TCP (or UDP, in the case of WebRTC) to provide a layer of abstraction for different types of data typically associated with web applications.

## Example: A simple web request

When you type a URL into your browser, several layers of networking protocols spring into action. Let's break down how these layers work together to retrieve a simple web page over HTTP on TCP.

First, we use DNS to convert a human-readable domain name like hellointerview.com into an IP address like 32.42.52.62. Then, a series of carefully orchestrated steps begins. We set up a TCP connection over IP, send our HTTP request, get a response, and tear down the connection.

- **DNS Resolution:** The client starts by resolving the domain name of the website to an IP address using DNS (Domain Name System).

- **TCP Handshake:** The client initiates a TCP connection with the server using a three-way handshake:
    - **SYN:** The client sends a SYN (synchronize) packet to the server to request a connection.
    - **SYN-ACK:** The server responds with a SYN-ACK (synchronize-acknowledge) packet to acknowledge the request.
    - **ACK:** The client sends an ACK (acknowledge) packet to establish the connection.

- **HTTP Request:** Once the TCP connection is established, the client sends an HTTP GET request to the server to request the web page.

- **Server Processing:** The server processes the request, retrieves the requested web page, and prepares an HTTP response. (This is usually the only latency most SWE's think about and control!)

- **HTTP Response:** The server sends the HTTP response back to the client, which includes the requested web page content.

- **TCP Teardown:** After the data transfer is complete, the client and server close the TCP connection using a four-way handshake:
    - **FIN:** The client sends a FIN (finish) packet to the server to terminate the connection.
    - **ACK:** The server acknowledges the FIN packet with an ACK.
    - **FIN:** The server sends a FIN packet to the client to terminate its side of the connection.
    - **ACK:** The client acknowledges the server's FIN packet with an ACK.

## Networking layer protocols

The first layer in our journey are the network layer protocols. This layer is dominated by the IP protocol, which is responsible for routing and addressing. In a system, nodes are assigned IPs usually by a DHCP server when they boot up.

These assigned IP addresses are called public IPs and are used to identify devices on the internet. The most important thing about them is that internet routing infrastructure is optimized to route traffic between public IPs and knows where they are.

## Transport layer protocols

The transport layer is where we establish end-to-end communication between applications. They give us some some guarantees instead of handing us a jumbled mess of packets. The three primary protocols at this layer are TCP, UDP, and QUIC, each with distinct characteristics that make them suitable for different use cases.

### UDP: fast but unreliable

User Datagram Protocol (UDP) is the machinegun of protocols. It offers few features on top of IP but is very fast. It provides a simpler, connectionless service with no guarantees of delivery, ordering, or duplicate protection.
If you write an application that receives UDP datagrams, you'll be able to see where they came from (i.e. the source IP address and port) and where they're going (i.e. the destination IP address and port). But that's it! The rest is a binary blob.

#### Key characteristics of UDP include:

- **Connectionless:** No handshake or connection setup
- **No guarantee of delivery:** Packets may be lost without notification
- **No ordering:** Packets may arrive in a different order than sent
- **Lower latency:** Less overhead means faster transmission

UDP is perfect for applications where speed is more important than reliability, such as live video streaming, online gaming, VoIP, and DNS lookups.

### TCP: reliable but with overhead

Transmission Control Protocol (TCP) is the workhorse of the internet. It provides reliable, ordered, and error-checked delivery of data. It establishes a connection through a three-way handshake and maintains that connection throughout the communication session.

#### Key characteristics of TCP include:

- **Connection-oriented:** Establishes a dedicated connection before data transfer
- **Reliable delivery:** Guarantees that data arrives in order and without errors
- **Flow control:** Prevents overwhelming receivers with too much data
- **Congestion control:** Adapts to network congestion to prevent collapse

TCP is ideal for applications where data integrity is critical — that is, basically everything where UDP is not a good fit.

### When to choose which protocol ?

You might choose UDP when:
- Low latency is critical (real-time applications, gaming)
- Some data loss is acceptable (media streaming)
- You're handling high-volume telemetry or logs where occasional loss is acceptable
- You don't need to support web browsers (or you have an alternative for that client)

In all other cases, you can choose TCP.

| Feature | UDP | TCP |
|---------|---------|---------|
| Connection | Connectionless | Connection-oriented |
| Reliability | Best-effort delivery | Guaranteed delivery |
| Ordering | No ordering guarantees | Maintains order |
| Flow Control | No | Yes |
| Congestion Control | No | Yes |
| Header Size | 8 bytes | 20–60 bytes |
| Speed | Faster | Slower due to overhead |
| Use Cases | Streaming, gaming, VoIP | Everything else |

## Application layer protocols

These protocols define how applications communicate and are built on top of the transport layer protocols

### HTTP/HTTPS

Hypertext Transfer Protocol (HTTP) is the de-facto standard for data communication on the web. It's a request-response protocol where clients send requests to servers, and servers respond with the requested data.

- **Request methods:** GET, POST, PUT, DELETE, etc.
- **Status codes:** 200 OK, 404 Not Found, 500 Server Error, etc.
- **Headers:** Metadata about the request or response
- **Body:** The actual content being transferred

HTTPS adds a security layer (TLS/SSL) to encrypt communications, protecting against eavesdropping and man-in-the-middle attacks. If you're building a public website you're going to be using HTTPS without exception. Generally speaking this means that the contents of your HTTP requests and responses are encrypted and safe in transit.

### REST: Simple and flexible

In RESTful API design, the primary challenge is to model your resources and the operations you can perform on them. RESTful API's take advantage of the HTTP methods or verbs together with some opinionated conventions about the paths and the body of the request. They often use JSON to represent the resources in both the request and response bodies — although it's not strictly required.

A simple RESTful API might look like this (where User is a JSON object representing a user):
```json
    GET /users/{id} -> User
```
Here we're using the HTTP method "GET" to indicate that we're requesting a resource. The {id} is a placeholder for the resource ID, in this case the user ID of the user we want to retrieve.

When we want to update that user, we can use the HTTP method "PUT" to indicate that we're updating a pre-existing resource.

```json
    PUT /users/{id} -> User
    {
      "username": "john.doe",
      "email": "john.doe@example.com"
    }
```

We can also create new resources by using the HTTP method "POST". We'll include the body the content of the resource we want to create. Note that I'm not specifying an ID here because the server will assign one.

```json
    POST /users -> User
    {
      "username": "stefan.mai",
      "email": "stefan@hellointerview.com"
    }
```

Finally, resources can be nested to represent relationships between resources. For example, a user might have many posts, so we can represent that relationship by nesting the posts under the user resource.

```json
    GET /users/{id}/posts -> [Post]
```

### GraphQL: Flexible Data Fetching

GraphQL is a more recent API paradigm that allows clients to request exactly the data they need.

Here's the problem GraphQL solves: 

```
Frequently teams and systems are organized into frontend and backend. As an example, the frontend might be a mobile app and the backend a database-based API. When the frontend team wants to display a new page, they can either (a) cobble together a bunch of different requests to backend endpoints (imagine querying 1 API for a list of users and making 10 API calls to get their details), (b) create huge aggregation APIs which are hard to maintain and slow to change, or (c) write brand new APIs for every new page they want to display. None of these are particularly good solutions but it's easy to run into them with a standard REST API.
The problem with under-fetching is that you may need multiple requests and round trips. This adds overhead and latency to the page load.
```

GraphQL solves these problems by allowing the frontend team to flexibly query the backend for exactly the data they need. The backend can then respond with the data in the shape that the frontend needs it. This is a great fit for mobile apps and other use-cases where you want to reduce the amount of data transferred.

#### Where to use it ?

GraphQL is a great fit for use-cases where the frontend team needs to iterate quickly and adjust. They can flexibly query the backend for exactly the data they need. On the other hand, execution of these GraphQL queries can be a source of latency and complexity for the backend — sometimes involving the same bespoke backend code that we're trying to avoid. In practice, GraphQL finds its sweet spot with complex clients and when multiple teams are making wide queries to overlapping data.

We recommend bringing up GraphQL in cases where the problem is clearly focused on flexibility (e.g. the interviewer tells us we need to be able to adapt our apps quickly to changing requirements) or when the requirements in the interview are deliberately uncertain.

### gRPC: Efficient Service Communication

gRPC is a high-performance RPC (Remote Procedure Call) framework from Google (the "g") that uses HTTP/2 and Protocol Buffers. Think of Protocol Buffers like JSON but with a more rigid schema that allows for better performance and more efficient serialization. Here's an example of a Protocol Buffer definition for a User resource:

```json
    message User {
      string id = 1;
      string name = 2;
    }
```

Instead of a chunky JSON object with embedded schema (40 bytes), we have a binary encoding (15 bytes) of the same data with very skinny tags and variable length encoding of the strings. Less space and less CPU to parse!

#### Where to use it ?

Consider gRPC for internal service-to-service communication, especially when performance is critical or when latencies are dominated by the network rather than the work the server is doing.


### Server send events (SSE): Real-Time Push Communication

SSE is a nice hack on top of HTTP that allows a server to stream many messages, over time, in a single response from the server.

#### Where to Use It ?
You'll find SSE useful in system design interviews in situations where you want clients to get notifications or events as soon as they happen. SSE is a great option for keeping bidders up-to-date on the current price of an auction, for example.

### WebSockets: Real-Time Bidirectional Communication

WebSockets provide a persistent, TCP-style connection between client and server, allowing for real-time, bidirectional communication with broad support (including browsers). Unlike HTTP's request-response model, WebSockets enable servers to push data to clients without being prompted by a new request. Similarly clients can push data back to the server without the same wait.

Unlike the traditional HTTP protocol, where the client sends a request to the server and waits for a response, WebSockets allow both the client and server to send messages to each other independently and continuously after the connection is established.

#### How it Works

- Client initiates WebSocket handshake over HTTP (with a backing TCP connection)
- Connection upgrades to WebSocket protocol, WebSocket takes over the TCP connection
- Both client and server can send binary messages to each other over the connection
- The connection stays open until explicitly closed

#### Where to Use It
WebSockets come up in system design interviews when you need high-frequency, persistent, bi-directional communication between client and server. Think real-time applications, games, and other use-cases where you need to send and receive messages as soon as they happen.

## Handling failures in networking

The fallacy of "the network is reliable" is one of the most dangerous assumptions in distributed systems. Always design with the expectation that network calls will fail, be delayed, or return unexpected results.

### Timeouts and Retries with Backoff

The most elementary hygiene for handling failures is to use timeouts and retries. If we expect a request to take a certain amount of time, we can set a timeout and if the request takes too long we can give up and try again.
Retrying requests is a great strategy for dealing with transient failures. If a server is temporarily slow, we can retry the request and it will likely succeed. Having idempotent APIs is key here because we can retry the same request multiple times without causing issues.

### Backoff

Retries can be a double-edged sword, though. If we have a lot of retries, we may be retrying requests that are going to fail over and over again. This can actually make the problem worse!
This is why most retry strategies also include a backoff strategy. Instead of retrying immediately, we wait a short amount of time before retrying. If the request still fails, we wait a little longer. This gives the system time to recover and reduces the load on the system.

### Idempotency

Retries are cool except when they have side effects. Imagine a payment system where we're trying to charge a user $10 for something. If we retry the same request multiple times, we're going to charge the user $20 (or $2,000) instead of $10! Ouch.
This is why we need to make sure our APIs are idempotent. Idempotent APIs are APIs that can be called multiple times and they produce the same result every time. HTTP GET requests are common examples of idempotent APIs. While the content returned by a GET request may change, the act of fetching the content does not change the state of the system.

For our payment example, if we know a user is only ever going to buy one item per day, we can set an idempotency to the user's ID and the current date. On the server-side, we can check to see if we've already processed (or are currently processing) a request with that idempotency key and process it only once. User-friendly APIs will wait for the request to complete then send the results to all requesters.

### Circuit breakers

The last topic we see commonly in deep dives is how to handle cascading failures in a system. Senior candidates are frequently asked questions like “what happens when this service goes down”. Sometimes the answer is simple: “we fail and retry until it boots back up” — but occasionally that will introduce new problems for the system!

The key for your preparation is to familiarize yourself with scenarios where one failure might create new failures: a cascade of failures. Being able to identify these patterns and how to mitigate them is a great way to stand out in an interview.

Circuit breakers protect your system when network calls to dependencies fail repeatedly. Here's how they work:

- The circuit breaker monitors for failures when calling external services
- When failures exceed a threshold, the circuit "trips" to an open state
- While open, requests immediately fail without attempting the actual call
- After a timeout period, the circuit transitions to a "half-open" state
- A test request determines whether to close the circuit or keep it open

#### Where to Use It

Circuit breakers can be a great response when an interviewer is deep-diving on reliability, failure modes, or disaster recovery. Being able to mention circuit breakers and apply them in useful places is a great way to show off knowledge that otherwise is won at 3:00am battling a hardware failure when the system Just. Won’t. Come. Back. Up.
Some example sites to apply circuit breakers:

- External API calls to third-party services
- Database connections and queries
- Service-to-service communication in microservices
- Resource-intensive operations that might time out
- Any network call that could fail or become slow