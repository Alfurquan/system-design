# CAP Theorem

At its core, CAP theorem states that in a distributed system, you can only have two out of three of the following properties:

- **Consistency:** All nodes see the same data at the same time. When a write is made to one node, all subsequent reads from any node will return that updated value.

- **Availability:** Every request to a non-failing node receives a response, without the guarantee that it contains the most recent version of the data.

- **Partition Tolerance:** The system continues to operate despite arbitrary message loss or failure of part of the system (i.e., network partitions between nodes).

Here's the key insight that makes CAP theorem much simpler to reason about in interviews: In any distributed system, partition tolerance is a must. Network failures will happen, and your system needs to handle them.
This means that in practice, CAP theorem really boils down to a single choice: Do you prioritize consistency or availability when a network partition occurs?

## When to Choose Consistency

Some systems absolutely require consistency, even at the cost of availability:

- **Ticket Booking Systems:** Imagine if User A booked seat 6A on a flight, but due to a network partition, User B sees the seat as available and books it too. You'd have two people showing up for the same seat!

- **E-commerce Inventory:** If Amazon has one toothbrush left and the system shows it as available to multiple users during a network partition, they could oversell their inventory.

- **Financial Systems:** Stock trading platforms need to show accurate, up-to-date order books. Showing stale data could lead to trades at incorrect prices.

When to Choose Availability
The majority of systems can tolerate some inconsistency and should prioritize availability. In these cases, eventual consistency is fine. Meaning, the system will eventually become consistent, but it may take a few seconds or minutes.

- **Social Media:** If User A updates their profile picture, it's perfectly fine if User B sees the old picture for a few minutes.
- **Content Platforms (like Netflix):** If someone updates a movie description, showing the old description temporarily to some users isn't catastrophic.
- **Review Sites (like Yelp):** If a restaurant updates their hours, showing slightly outdated information briefly is better than showing no information at all.

The key question to ask yourself is: "Would it be catastrophic if users briefly saw inconsistent data?" If the answer is yes, choose consistency. If not, choose availability.

## CAP Theorem in System Design Interviews

If you prioritize consistency, your design might include:
- **Distributed Transactions:** Ensuring multiple data stores (like cache and database) remain in sync through two-phase commit protocols. This adds complexity but guarantees consistency across all nodes. This means users will likely experience higher latency as the system ensures data is consistent across all nodes.

- **Single-Node Solutions:** Using a single database instance to avoid propagation issues entirely. While this limits scalability, it eliminates consistency challenges by having a single source of truth.

- **Technology Choices:**
    - Traditional RDBMSs (PostgreSQL, MySQL)
    - Google Spanner
    - DynamoDB (in strong consistency mode)


If you prioritize availability, your design can include:
- **Multiple Replicas:** Scaling to additional read replicas with asynchronous replication, allowing reads to be served from any replica even if it's slightly behind. This improves read performance and availability at the cost of potential staleness.

- **Change Data Capture (CDC):** Using CDC to track changes in the primary database and propagate them asynchronously to replicas, caches, and other systems. This allows the primary system to remain available while updates flow through the system eventually.

- **Technology Choices:**
    - Cassandra
    - DynamoDB (in multiple availability zone configuration)
    - Redis clusters

## Different Levels of Consistency

- **Strong Consistency:** All reads reflect the most recent write. This is the most expensive consistency model in terms of performance, but is necessary for systems that require absolute accuracy like bank account balances. This is what we have been discussing so far.

- **Causal Consistency:** Related events appear in the same order to all users. This ensures logical ordering of dependent actions, such as ensuring comments on a post must appear after the post itself.

- **Read-your-own-writes Consistency:** Users always see their own updates immediately, though other users might see older versions. This is commonly used in social media platforms where users expect to see their own profile updates right away.

- **Eventual Consistency:** The system will become consistent over time but may temporarily have inconsistencies. This is the most relaxed form of consistency and is often used in systems like DNS where temporary inconsistencies are acceptable. This is the default behavior of most distributed databases and what we are implicitly choosing when we prioritize availability.