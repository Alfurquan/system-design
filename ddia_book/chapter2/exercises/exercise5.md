# 📌 Exercise 5: Recommendation Engine Traversal

## 🧩 Problem Statement

You are building a basic movie recommendation engine.

- Users rate movies on a platform (like 1 to 5 stars).
- If a user gives a rating of 4 or 5, it's considered a **like**.
- The engine recommends movies that are liked by users who liked the same movies as the target user.

You need to:

- Design data models for both:
  - A **relational database** (e.g., PostgreSQL or MySQL)
  - A **graph database** (e.g., Neo4j)

- Implement traversal steps (or equivalent queries) to:
  - Find users who liked the **same movie** as a given user.
  - Find **other movies** those users liked (excluding ones already rated by the given user).
  - (Optional) Rank recommendations by **number of mutual likes** (collaborative filtering lite).

---

## 🧠 Tasks

### 1. Schema Design

#### Relational DB

- Define:
  - Tables
  - Columns
  - Primary/Foreign Keys

#### Graph DB

- Define:
  - Node types (e.g., User, Movie)
  - Relationship types (e.g., LIKED)

---

### 2. Query/Traversal Design

Write **SQL** (for relational) or **Cypher** (for graph) to:

- Find users who **liked the same movie** as User A.
- From those users, find **other movies** they liked.
- Optionally, **exclude** movies already rated by User A.
- (Optional) Return movies **ordered by popularity** (number of similar users who liked them).

---

# Solution

## 1. Schema design

### Relational DB

#### Tables

**`User`**

| Column     | Type         | Notes          |
|------------|--------------|----------------|
| id         | UUID (PK)    | Unique ID      |
| name       | TEXT         |                |

---

**`Movie`**

| Column     | Type         | Notes          |
|------------|--------------|----------------|
| id         | UUID (PK)    | Unique ID      |
| name       | TEXT         |                |

---

**`Rating`**

| Column     | Type         | Notes                        |
|------------|--------------|------------------------------|
| movieId    | UUID (FK)    | References `movie.id`        |
| userId     | UUID (FK)    | References `user.id`         |
| rating     | DECIMAL      | Constaraint that between 1-5 |

---

### Graph DB

- Nodes: User and Movie will be nodes
- Relations: LIKED will be a relationship between User and movie

## 2. Query/Traversal Design

### Relational DB

- Find users who **liked the same movie** as User A.

```SQL
SELECT DISTINCT u2.id, u2.name
FROM User u1
JOIN Rating r1 ON u1.id = r1.userId
JOIN Rating r2 ON r1.movieId = r2.movieId
JOIN User u2 ON r2.userId = u2.id
WHERE u1.id = 'user_a_id' AND r1.rating >= 4 AND r2.rating >= 4;
```

- From those users, find **other movies** they liked.

```SQL
SELECT DISTINCT r2.movieId
FROM Rating r1
JOIN Rating r2 ON r1.userId = r2.userId
WHERE r1.userId = 'user_a_id' AND r1.rating >= 4 AND r2.rating >= 4
AND r2.movieId NOT IN (
    SELECT movieId FROM Rating WHERE userId = 'user_a_id'
);
```
- Optionally, **exclude** movies already rated by User A.

```SQL
SELECT DISTINCT r2.movieId
FROM Rating r1
JOIN Rating r2 ON r1.userId = r2.userId
WHERE r1.userId = 'user_a_id' AND r1.rating >= 4 AND r2.rating >= 4
AND r2.movieId NOT IN (
    SELECT movieId FROM Rating WHERE userId = 'user_a_id'
);
```
- (Optional) Return movies **ordered by popularity**.

```SQL
SELECT r2.movieId, COUNT(*) AS like_count
FROM Rating r1
JOIN Rating r2 ON r1.userId = r2.userId
WHERE r1.userId = 'user_a_id' AND r1.rating >= 4 AND r2.rating >= 4
AND r2.movieId NOT IN (
    SELECT movieId FROM Rating WHERE userId = 'user_a_id'
)
GROUP BY r2.movieId
ORDER BY like_count DESC;
```
### Graph DB
- Find users who **liked the same movie** as User A.

From the target user node, traverse LIKED edges to get movies. From those movies, traverse incoming LIKED edges to get other users who liked them.

- Find other movies those users liked.

From those users in above point, traverse out LIKED edges to new movies.

- (optional) Return movies ordered by popularity.

Count frequency per movie and rank.



