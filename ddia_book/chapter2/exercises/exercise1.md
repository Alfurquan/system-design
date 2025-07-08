# Exercise 1: 📝 Design a Data Model for a Blogging Platform (like Medium)

## 📌 Problem Statement

Design the data model for a blogging platform similar to Medium:

- Authors write **articles**.
- Articles have **tags** and **comments**.
- Users can **like** both articles and comments.
- An article can have **multiple tags**.
- Articles and comments have **timestamps** and **authors**.

---

## ⚙️ Model Approaches

Design using **both** data modeling paradigms:

1. **Relational Model**  
   Define tables, keys, and relationships.

2. **Document Model**  
   Define a sample JSON structure for an article document.

---

## 🧠 Your Tasks

### 1. Relational Model

Design the relational schema including:

- Table names  
- Columns  
- Relationships (e.g., one-to-many, many-to-many)  
- Primary and foreign keys

### 2. Document Model

Model the same system using a **document-oriented database**:

- Define what a **sample article document** would look like
- Decide what to **embed** vs. what to **reference**

---

## ⚖️ Trade-offs to Consider

| Factor               | Relational Model                           | Document Model                            |
|----------------------|--------------------------------------------|-------------------------------------------|
| Schema Flexibility   | Low – changes require migrations           | High – schema can evolve freely           |
| Join Support         | Strong – native support                    | Weak – joins must be handled in app code  |
| Performance          | May degrade with joins on large datasets   | Optimized for read-heavy operations       |
| Data Duplication     | Low – normalized data                      | Medium/High – depending on embedded docs  |
| Use Case Fit         | Structured transactional data              | Aggregated, read-optimized data access    |

---

## ✅ Output Expected

- Relational schema diagrams or table definitions
- JSON structure representing an article with nested data
- Commentary on modeling decisions and trade-offs

---

# Solution

# Exercise 1: Blogging Platform – Data Modeling

## ✅ Relational Model

### Tables

#### `User`
| Column     | Type         | Notes          |
|------------|--------------|----------------|
| id         | UUID (PK)    | Unique ID      |
| name       | TEXT         |                |
| bio        | TEXT         |                |

---

#### `Article`
| Column     | Type         | Notes                    |
|------------|--------------|--------------------------|
| id         | UUID (PK)    |                          |
| title      | TEXT         |                          |
| content    | TEXT         |                          |
| authorId   | UUID (FK)    | References `User.id`     |
| createdAt  | TIMESTAMP    |                          |

---

#### `Comment`
| Column     | Type         | Notes                           |
|------------|--------------|---------------------------------|
| id         | UUID (PK)    |                                 |
| articleId  | UUID (FK)    | References `Article.id`         |
| userId     | UUID (FK)    | References `User.id`            |
| text       | TEXT         |                                 |
| createdAt  | TIMESTAMP    |                                 |

---

#### `Tag`
| Column     | Type         | Notes             |
|------------|--------------|-------------------|
| id         | UUID (PK)    |                   |
| text       | TEXT UNIQUE  | Avoid duplicate tags |

---

#### `Article_Tag`
| Column     | Type         | Notes                        |
|------------|--------------|------------------------------|
| articleId  | UUID (FK)    | References `Article.id`      |
| tagId      | UUID (FK)    | References `Tag.id`          |
| PRIMARY KEY | (articleId, tagId) | Composite Key        |

---

#### `Article_Like`
| Column     | Type         | Notes                        |
|------------|--------------|------------------------------|
| articleId  | UUID (FK)    | References `Article.id`      |
| userId     | UUID (FK)    | References `User.id`         |
| PRIMARY KEY | (articleId, userId) | Composite Key      |

---

#### `Comment_Like`
| Column     | Type         | Notes                        |
|------------|--------------|------------------------------|
| commentId  | UUID (FK)    | References `Comment.id`      |
| userId     | UUID (FK)    | References `User.id`         |
| PRIMARY KEY | (commentId, userId) | Composite Key     |

---

### Notes:
- **1:N relationships** modeled via FKs (e.g., Article to Comments).
- **M:N relationships** handled via join tables (Tags, Likes).
- Embedding author/user info avoided for normalization.
- Could add **counters (denormalized)** for faster read performance if needed later.

---

## ✅ Document Model

### Sample `Article` Document (JSON)
```json
{
  "id": "article123",
  "title": "Understanding Data Models",
  "content": "This article explains data modeling concepts...",
  "author": {
    "id": "author456",
    "name": "John Doe",
    "bio": "Tech writer and data enthusiast"
  },
  "createdAt": "2023-10-01T12:00:00Z",
  "tags": [
    { "id": "tag789", "text": "Data Modeling" },
    { "id": "tag101", "text": "Database Design" }
  ],
  "comments": [
    {
      "id": "comment112",
      "text": "Great article!",
      "user": { "id": "user113", "name": "Alice" },
      "createdAt": "2023-10-01T12:30:00Z",
      "likes": {
        "count": 1,
        "likedBy": [{ "userId": "user114" }]
      }
    },
    {
      "id": "comment114",
      "text": "Very informative.",
      "user": { "id": "user115", "name": "Bob" },
      "createdAt": "2023-10-01T12:45:00Z",
      "likes": {
        "count": 2,
        "likedBy": [
          { "userId": "user116" },
          { "userId": "user117" }
        ]
      }
    }
  ],
  "likes": {
    "count": 2,
    "likedBy": [
      { "userId": "user118" },
      { "userId": "user119" }
    ]
  }
}
```

## Trade-offs
### Relational Model
- **Schema Flexibility**: Low, requires migrations for changes.
- **Join Support**: Strong, native support for complex queries.
- **Performance**: May degrade with joins on large datasets.
- **Data Duplication**: Low, normalized data reduces redundancy.
- **Use Case Fit**: Best for structured transactional data.
### Document Model
- **Schema Flexibility**: High, schema can evolve without migrations.
- **Join Support**: Weak, joins must be handled in application code.
- **Performance**: Optimized for read-heavy operations, especially with embedded documents.
- **Data Duplication**: Medium/High, depending on how much data is embedded.
- **Use Case Fit**: Ideal for aggregated, read-optimized data access.
### Conclusion
Here for the blogging platform, the **document model** is more flexible and better suited for read-heavy operations with nested data like comments and likes. The **relational model** provides strong consistency and complex querying capabilities but may require more effort to maintain as the schema evolves.


