# 🧩 Exercise 2 – Social Graph Design

## 📝 Problem Statement

You're building the backend for a social networking app (like Twitter or Instagram). The main feature is that users can follow other users. You need to design the data model for this follow relationship, with the following operations supported efficiently:

---

## 🔧 Core Functional Requirements

You need to model the "User Follows User" relationship with support for:

- **Follow a user**  
  _e.g., User A follows User B_

- **Unfollow a user**

- **Check if User A follows User B**

- **Fetch followers of a user**  
  _e.g., who follows User B_

- **Fetch users followed by a user**  
  _e.g., who User A is following_

- **Get mutual follows**  
  _e.g., who both User A and User B follow_

- **Suggested follows** *(Optional, stretch goal)*  
  _e.g., "users followed by people you follow"_

---

## ⚙️ Performance Considerations

For the above operations, consider:

- **Read vs. write performance**: Some operations happen more frequently than others.
- **Fan-out scale**: Some users may follow millions, or be followed by millions (e.g., celebrities).
- **Latency**: Some queries are on hot paths (e.g., home feed needs "who you follow").

---

## 🧠 Design Task

You need to provide two designs:

### 1️⃣ Relational Model

- Define schema for users and follow relationships.
- Include indexes, constraints, and justifications for your design choices.
- Explain how each operation will be implemented via SQL queries.
- Mention scaling concerns (e.g., for users with huge follower counts).

---

### 2️⃣ Alternative Models

Pick at least one alternative approach:

- Graph DB Model (e.g., Neo4j)
- Document Model
- Key-Value / Adjacency List approach
- Inverted index style

Explain:

- How the data would be stored
- How the same operations would be performed
- Trade-offs of this model vs. the relational one

---

## 🎯 Output Requirements

For each model:

- 📊 **Schema or Data Format**
- 🔍 **How each core operation would be implemented**
- ⚖️ **Trade-offs in performance, flexibility, and scalability**
- 🔐 *Optional*: Brief thoughts on **access control or privacy** (e.g., private accounts)

--

# Solution

## 1️⃣ Relational Model

### Tables

#### `User`
| Column     | Type         | Notes          |
|------------|--------------|----------------|
| id         | UUID (PK)    | Unique ID      |
| name       | TEXT         |                |
| bio        | TEXT         |                |

#### `Followers`
| Column     | Type         | Notes                 |
|------------|--------------|-----------------------|
| followerId | UUID (FK)    | References `User.id`  |
| followeeId | UUID (FK)    |                       |

### How the operations will be performed ?

- **Follow a user**  
  We can write insert statement in the followers table
  ```SQL
    INSERT INTO Followers (followerId, followeeId) VALUES ('userA_id', 'userB_id');
  ```

- **Unfollow a user**
    We can write delete statement in the followers table
    ```SQL
        DELETE FROM Followers WHERE followerId = 'userA_id' AND followeeId = 'userB_id';
    ```

- **Check if User A follows User B**
    We can write a select statement to check if a record exists
    ```SQL
        SELECT EXISTS(SELECT 1 FROM Followers WHERE followerId = 'userA_id' AND followeeId = 'userB_id');
    ```

- **Fetch followers of a user**  
    We can write a select statement to get all followers of a user
    ```SQL
        SELECT followerId FROM Followers WHERE followeeId = 'userB_id';
    ```

- **Fetch users followed by a user**  
    We can write a select statement to get all users followed by a user
    ```SQL
        SELECT followeeId FROM Followers WHERE followerId = 'userA_id';
    ```

- **Get mutual follows**  
    We can write a join query to find mutual follows
    ```SQL
        SELECT f1.followeeId 
        FROM Followers f1 
        JOIN Followers f2 ON f1.followeeId = f2.followeeId 
        WHERE f1.followerId = 'userA_id' AND f2.followerId = 'userB_id';
    ```
- **Suggested follows** *(Optional)*
    We can write a query to find users followed by people that User A follows
    ```SQL
        SELECT DISTINCT f2.followeeId 
        FROM Followers f1 
        JOIN Followers f2 ON f1.followeeId = f2.followerId 
        WHERE f1.followerId = 'userA_id' AND f2.followeeId != 'userA_id';
    ```

### Trade-offs
- **Performance**: Relational databases can handle large datasets, but joins can become expensive with many followers.
- **Flexibility**: Adding new features (like blocking users) may require schema changes.
- **Scalability**: Horizontal scaling can be challenging; sharding by user ID may be necessary for very large datasets.
### Scaling Concerns
- **Fan-out scale**: For users with millions of followers, the `Followers` table can grow large. Indexing `followerId` and `followeeId` is crucial for performance.
- **Latency**: Caching frequently accessed data (like follower counts) can help reduce latency for hot paths.

### Access Control or Privacy
- Implementing private accounts can be done by adding a `private` boolean column in the `User` table.
- When a user follows another, check if the followee's account is private before allowing the follow operation.

## 2️⃣ Alternative Models

### Document Model (e.g., MongoDB)
In a document-oriented database, we can model the user and their follows as follows:

#### `User` Document
```json
{
  "id": "userA_id",
  "name": "User A",
  "bio": "Bio of User A",
  "follows": [
    { "followeeId": "userB_id" },
    { "followeeId": "userC_id" }
  ]
}
```
### How the operations will be performed?
- **Follow a user**  
  Update the user's document to add the followee
  ```json
  db.users.updateOne(
    { "id": "userA_id" },
    { $addToSet: { "follows": { "followeeId": "userB_id" } } }
  );
  ```
- **Unfollow a user**
  Update the user's document to remove the followee
  ```json
  db.users.updateOne(
    { "id": "userA_id" },
    { $pull: { "follows": { "followeeId": "userB_id" } } }
  );
  ```
- **Check if User A follows User B**
    Query the user's document to check if the followee exists
    ```json
    db.users.findOne(
        { "id": "userA_id", "follows.followeeId": "userB_id" }
    );
    ```
- **Fetch followers of a user**
```json
    db.users.find(
        { "follows.followeeId": "userB_id" },
        { "id": 1, "name": 1 }
    );
```
- **Fetch users followed by a user**
```json
    db.users.findOne(
        { "id": "userA_id" },
        { "follows": 1 }
    );
```
- **Get mutual follows**
```json
    db.users.aggregate([
        { $match: { "id": "userA_id" } },
        { $lookup: {
            from: "users",
            localField: "follows.followeeId",
            foreignField: "follows.followeeId",
            as: "mutualFollows"
        }},
        { $unwind: "$mutualFollows" },
        { $match: { "mutualFollows.id": "userB_id" } }
    ]);
```
- **Suggested follows** *(Optional)*
```json
    db.users.aggregate([
        { $match: { "id": "userA_id" } },
        { $lookup: {
            from: "users",
            localField: "follows.followeeId",
            foreignField: "follows.followerId",
            as: "suggestedFollows"
        }},
        { $unwind: "$suggestedFollows" },
        { $match: { "suggestedFollows.id": { $ne: "userA_id" } } }
    ]);
```
### Trade-offs
- **Performance**: Document databases can handle large datasets efficiently, especially for read-heavy operations.
- **Flexibility**: Schema can evolve easily; new fields can be added without migrations.
- **Scalability**: Document databases are designed for horizontal scaling, making them suitable for large user bases.
- **Data Duplication**: Some data may be duplicated across documents (e.g., user names), which can lead to consistency issues.
### Access Control or Privacy
- Implementing private accounts can be done by adding a `private` field in the user document.
- When a user follows another, check if the followee's account is private before allowing the follow operation.
## Conclusion
In this exercise, we explored two different data models for a social graph: a relational model and a document model. The relational model provides strong consistency and complex querying capabilities, while the document model offers flexibility and scalability for read-heavy operations. Each model has its trade-offs, and the choice depends on the specific requirements of the application, such as read vs. write performance, schema flexibility, and scalability needs.

For a social networking app, the **document model** is often more suitable due to its flexibility and ability to handle large datasets efficiently, especially when user relationships are read-heavy. The **relational model** can still be used effectively, particularly when strong consistency and complex queries are required, but may require more effort to maintain as the schema evolves.

