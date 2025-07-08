## 📌 Exercise 4: Schema Evolution Scenario

### 🧩 Problem Statement

You are working on a user profile system that initially supported the following fields:

```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "123-456-7890"
}
```

Now, the product team wants to evolve the schema to support:

- A `socialHandles` field, such as:
  - `twitter`: `@janedoe`
  - `linkedin`: `linkedin.com/in/janedoe`
  - `github`: `github.com/janedoe`

- Later, a nested `preferences` object, for example:
  ```json
  {
    "preferences": {
      "theme": "dark",
      "notifications": {
        "email": true,
        "sms": false
      }
    }
  }
  ```

---

### 🎯 Your Tasks

#### 🗄️ Relational Database

- How would you evolve the schema to accommodate the new fields in a relational model?
- What are the pros and cons of different approaches?

#### 📄 Document Database

- How would the schema evolve in a document model like MongoDB?
- How would you manage backward compatibility with old documents?

#### 🌐 API Stability

- What challenges arise when you change the data model but want to keep APIs stable for clients?
- How would you handle these changes in API versions or responses?

---


# 📘 Solution: Schema Evolution Scenario

## 🗄️ Relational Database

### 🔹 Approach 1: Semi-structured Columns (String-encoded)

We add new columns `social_handles` and `preferences` of type `TEXT` and store serialized values such as:

- `social_handles`: `"twitter:@janedoe,github:janedoe"`
- `preferences`: `"theme:dark,notifications:email:true,sms:false"`

#### ✅ Pros
- Easy to implement initially.
- No schema migration needed for future additions (e.g., new social platforms or preferences).

#### ❌ Cons
- Poor data integrity — lacks type safety and validation.
- Complex parsing/querying, e.g., filtering users by theme or handle.
- Indexing on subfields is non-trivial or unsupported.
- Maintenance becomes difficult as field formats evolve.

---

### 🔹 Approach 2: Explicit Columns

Add separate columns for each field:

- `twitter_handle`, `github_handle`
- `theme`, `email_notifications`, `sms_notifications`

#### ✅ Pros
- Structured, normalized schema with clear types.
- Easy to query, index, and validate at the DB level.
- Cleaner migrations with SQL tools and ORMs.

#### ❌ Cons
- Schema changes needed for every new field (e.g., `linkedin_handle`).
- Requires backfills and migrations at scale.
- Risk of creating wide tables with many optional fields.

---

### 🔹 Approach 3 (Optional): Flexible JSON Columns

Use JSON/JSONB columns (e.g., in PostgreSQL):

- `social_handles JSONB`
- `preferences JSONB`

#### ✅ Pros
- Balance between flexibility and structure.
- Allows indexing on nested fields (GIN indexes).
- Cleaner than string blobs, supports structured queries.

#### ❌ Cons
- Still lacks enforced schema unless validated at app level.
- ORM support may vary.
- Harder to write strongly typed queries.

---

## 📄 Document Database

In a document store like MongoDB, schema evolution is more natural.

### Sample Document
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "123-456-7890",
  "social_handles": {
    "twitter": "@janedoe",
    "github": "github.com/janedoe"
  },
  "preferences": {
    "theme": "dark",
    "notifications": {
      "email": true,
      "sms": false
    }
  },
  "schema_version": 2
}
```

### ✅ Pros
- Flexible: Fields can be added without changing schema or migrating old documents.
- Nested structures provide semantic grouping.
- Supports partial updates (`$set`, `$unset`) and dynamic queries.

### ❌ Cons
- No automatic schema validation unless enforced using validators (e.g., MongoDB's JSON Schema or Mongoose).
- Old documents may lack new fields → can break clients if not handled properly.
- Application logic becomes responsible for handling multiple shapes of documents.

### 🔄 Handling Backward Compatibility
- Use application-level defaults for missing fields.
- Introduce a `schema_version` field in each document.
- Use migration scripts for background upgrades if needed.
- Write resilient code that gracefully handles absent fields.

---

## 🌐 API Stability

### ❗ Challenges with Model Evolution
- Older clients may break if they depend on deprecated fields or missing new ones.
- JSON contract mismatches lead to client-side bugs.
- Managing dual logic for old and new schema shapes in the backend can get messy.

### 🛠️ Strategies to Ensure Stability

#### 1. **Backward Compatibility in API Code**
- Use optional fields in responses.
- Populate defaults for missing values from DB before sending response.
- Avoid removing fields abruptly.

#### 2. **API Versioning**
- Create `/api/v1/users` for legacy format.
- Create `/api/v2/users` with evolved schema and payloads.
- Enables gradual client migration and parallel support.

#### 3. **GraphQL or Field Projections**
- Clients explicitly select fields, reducing breakage when new fields are added.
- Reduces over-fetching and avoids tight coupling with response structure.

#### 4. **Feature Flags / Capability Detection**
- Return fields conditionally based on client capabilities (e.g., via headers or tokens).

#### 5. **Contract Management Tools**
- Use OpenAPI / Swagger or Protobuf (for gRPC) to ensure stable and documented interfaces.
- Automatically validate schema evolution during CI/CD.

---