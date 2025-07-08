# 📚 Data Modeling Cheat Sheet: Document vs Graph Models

## 📄 Document Model (e.g., MongoDB)

### ✅ Best For
- Nested/aggregated documents (e.g., blog posts with comments, user with address and orders)
- Read-heavy applications
- Schema flexibility
- Use cases where joins are not frequently needed

---

### 🧠 Core Concepts

| Concept               | MongoDB Example                                         | Notes                                         |
|------------------------|---------------------------------------------------------|-----------------------------------------------|
| Create Document        | `db.users.insertOne({...})`                            | Insert a new document                         |
| Find Document          | `db.users.find({ name: "Alice" })`                     | Simple query                                  |
| Update Fields          | `db.users.updateOne({ id }, { $set: {...} })`          | Update selected fields                        |
| Add to Array           | `$addToSet`, `$push`                                   | Push values into an array                     |
| Remove from Array      | `$pull`                                                | Pull specific values from array               |
| Lookup (Join)          | `$lookup`                                              | Expensive join simulation                     |
| Aggregation Pipeline   | `db.collection.aggregate([...])`                       | Multi-stage document transformation           |

---

### 📝 Example User Document

```json
{
  "id": "user123",
  "name": "Alice",
  "bio": "Loves databases",
  "follows": [
    { "followeeId": "user456" },
    { "followeeId": "user789" }
  ]
}
```

---

### ⚖️ Trade-Offs: Document Model

| Pros                                         | Cons                                          |
|---------------------------------------------|-----------------------------------------------|
| Schema flexibility                          | Poor support for multi-document transactions  |
| Fast reads (denormalized, nested)           | Joins are not efficient                       |
| Scales horizontally easily                  | Data duplication                              |
| Great for event logs, user profiles, etc.   | Embedded arrays can grow unbounded            |

---

### 🧮 Tips for Usage
- Denormalize when reads are more frequent than writes.
- Embed if subdocuments are only relevant within the parent.
- Reference (foreign key-style) if document size may explode.

---

## 🔗 Graph Model (e.g., Neo4j)

### ✅ Best For
- Social networks (friend-of-friend, followers)
- Recommendations and connections
- Fraud detection and pathfinding
- Any highly interconnected dataset

---

### 🧠 Core Concepts (Cypher Syntax)

| Concept                 | Example Cypher Query                                     | Description                                   |
|-------------------------|----------------------------------------------------------|-----------------------------------------------|
| Create Node             | `CREATE (a:User {name: "Alice"})`                        | Create a user node                            |
| Create Relationship     | `CREATE (a)-[:FOLLOWS]->(b)`                             | Directed edge                                 |
| Match Node              | `MATCH (a:User {name: "Alice"}) RETURN a`               | Query a node                                  |
| Traverse Relationship   | `MATCH (a)-[:FOLLOWS]->(b) RETURN b.name`               | One-hop traversal                             |
| Mutual Follows          | `MATCH (a)-[:FOLLOWS]->(x)<-[:FOLLOWS]-(b) RETURN x`     | Two-hop mutual follows                        |
| Friend-of-Friend        | `MATCH (a)-[:FOLLOWS]->()-[:FOLLOWS]->(c) RETURN c`      | Suggested follows                             |
| Count Followers         | `MATCH (a)<-[:FOLLOWS]-(b) RETURN count(b)`              | Count incoming edges                          |

---

### 🧩 Sample Graph

```cypher
CREATE (alice:User {name: "Alice"})
CREATE (bob:User {name: "Bob"})
CREATE (carol:User {name: "Carol"})
CREATE (alice)-[:FOLLOWS]->(bob)
CREATE (bob)-[:FOLLOWS]->(carol)
CREATE (carol)-[:FOLLOWS]->(alice)
```

---

### ⚖️ Trade-Offs: Graph Model

| Pros                                         | Cons                                          |
|---------------------------------------------|-----------------------------------------------|
| Excellent for traversals and relationships  | Not ideal for flat or tabular data            |
| Flexible schema                              | Tooling & developer ecosystem less mature     |
| Easy to model real-world networks           | Query performance may degrade with depth      |
| Intuitive graph queries using Cypher        | Horizontal scaling is complex                 |

---

## ⚔️ When to Use Which?

| Use Case                              | Best Model     |
|---------------------------------------|----------------|
| Blog with nested comments             | Document       |
| Banking system                        | Relational     |
| Social network (followers, friends)   | Graph          |
| Product catalog with reviews          | Document       |
| Deep link recommendation (LinkedIn)   | Graph          |
| Simple CRUD application               | Relational     |
| Event log tracking                    | Document       |
| Real-time fraud detection             | Graph          |

---

## 🧠 Interview Tips
- Always ask about **access patterns** before choosing a model.
- Focus on **read/write frequency**, **data relationships**, and **scale**.
- Mention **denormalization**, **fan-out**, and **query complexity** as trade-offs.

---

## 📌 Quick Summary

| Feature              | Document DB             | Graph DB                 |
|----------------------|--------------------------|---------------------------|
| Schema Flexibility   | High                     | High                      |
| Read Performance     | High (if embedded)       | High (for deep queries)   |
| Write Performance    | Medium (depends on size) | Medium                    |
| Relationships        | Poor                     | Excellent                 |
| Joins                | Limited                  | Native via edges          |
| Scaling              | Easy (horizontal)        | Complex (not trivial)     |
| Use Cases            | CMS, logs, user profiles | Social graphs, paths      |

---