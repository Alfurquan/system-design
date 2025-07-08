# 📦 Exercise 3 – Product Catalog Data Modeling

## 💬 Problem Statement

You’re building an e-commerce platform that allows users to browse and search through a catalog of products. Each product can:

- Belong to multiple categories
- Have multiple variants
- Include specifications, pricing info, stock status, and reviews

You need to design the data model that supports:

- Efficient browsing by category/sub-category
- Searching products by attributes (e.g., color, size, brand)
- Handling product variants (e.g., color, size combinations)
- Managing real-time stock updates
- Supporting user reviews with ratings and comments

---

## 🎯 Your Task

Design data models using the following approaches:

### 1️⃣ Relational Model

- Define all necessary tables with primary/foreign keys
- Show how categories and variants are modeled
- Show how stock updates and reviews are handled

### 2️⃣ Document Model

- Design a sample JSON document representing a product with:
  - Multiple variants
  - Categories
  - Reviews
- Explain which parts you **embed** vs **reference**, and why

### 3️⃣ Graph Model *(Optional)*

- Sketch out a high-level idea (verbally or diagrammatically) of how:
  - Products
  - Categories
  - Users
  - Reviews  
  can be modeled as a graph

- Describe how a **traversal** might work to find:
  - “Products liked by people who reviewed similar products”

---

## 📌 Focus on:

- **Schema flexibility**
- **Query performance**
- **Update patterns**
- **Trade-offs** (e.g., duplication vs joins)
- **Scalability**

---

# Solution

## 1️⃣ Relational Model

### Tables

#### `User`
| Column     | Type         | Notes          |
|------------|--------------|----------------|
| id         | UUID (PK)    | Unique ID      |
| name       | TEXT         |                |

---

#### `Category`
| Column     | Type         | Notes                               |
|------------|--------------|-------------------------------------|
| id         | UUID (PK)    | Unique ID                           |
| name       | TEXT         |                                     |
| parent_id  | UUID (FK)    | Self-referential for sub-categories |
| description| TEXT         |                                     |

---

#### `Product`
| Column     | Type         | Notes                     |
|------------|--------------|---------------------------|
| id         | UUID (PK)    | Unique ID                 |
| name       | TEXT         |                           |
| description| TEXT         |                           |
| price      | DECIMAL      |                           |
| brand_id  | UUID (FK)    | Foreign key to `Brand`     |
| created_at | TIMESTAMP    |                           |

---

##### `ProductCategory`
| Column     | Type         | Notes                     |
|------------|--------------|---------------------------|
| product_id | UUID (FK)    | Foreign key to `Product`  |
| category_id| UUID (FK)    | Foreign key to `Category` |


#### `Variant`
| Column     | Type         | Notes                     |
|------------|--------------|---------------------------|
| id         | UUID (PK)    | Unique ID                 |
| product_id | UUID (FK)    | Foreign key to `Product`  |
| color      | TEXT         |                           |
| size       | TEXT         |                           |
| stock      | INTEGER      |                           |
---

#### `Review`
| Column     | Type         | Notes                     |
|------------|--------------|---------------------------|
| id         | UUID (PK)    | Unique ID                 |
| text       | TEXT         |                           |
| rating     | INTEGER      |                           |
| user_id    | UUID (FK)    | Foreign key to `User`     |
| product_id | UUID (FK)    | Foreign key to `Product`  |
| created_at | TIMESTAMP    |                           |

---

#### `Brand`
| Column     | Type         | Notes                     |
|------------|--------------|---------------------------|
| id         | UUID (PK)    | Unique ID                 |
| name       | TEXT         |                           |
| description| TEXT         |                           |

---

#### How stock updates and reviews are handled ?
- Stock updates can be handled by updating the `stock` column in the `Variant` table whenever a purchase is made or stock is replenished.
- Reviews are stored in the `Review` table, linked to both the `User` and `Product` tables via foreign keys. Each review includes a rating and text, allowing users to provide feedback on products.

### 2️⃣ Document Model
Here is a sample JSON document representing a product:

```json
{
  "id": "product-123",
  "name": "Running Shoes",
  "description": "High-performance running shoes",
  "brandId": "brand-456",
  "categoryIds": ["category-789", "category-101"],
  "variants": [
    {
      "id": "variant-1",
      "color": "Red",
      "size": "10",
      "stock": 50,
      "price": 59.99
    },
    {
      "id": "variant-2",
      "color": "Blue",
      "size": "10",
      "stock": 30,
      "price": 59.99
    }
  ],
  "reviews": [
    {
      "user_id": "user-456",
      "text": "Great shoes for running!",
      "rating": 5,
      "created_at": "2023-10-01T12:00:00Z"
    }
  ]
}

{
    "categories": [
        {
        "id": "category-789",
        "name": "Footwear",
        "parent_id": null,
        "description": "All types of footwear"
        },
        {
        "id": "category-101",
        "name": "Sports",
        "parent_id": "category-789",
        "description": "Sports equipment and apparel"
        }
    ],
    "brand": {
        "id": "brand-456",
        "name": "BrandName",
        "description": "Leading brand in sportswear"
    }
}

```
### Embedding vs Referencing
- **Embedding**: 
  - Variants and reviews are embedded within the product document. This allows for fast access to all product-related information in a single read operation, which is beneficial for performance when displaying product details.
- **Referencing**:
  - Categories are referenced to allow for a more flexible category structure, where categories can be shared across multiple products without duplication. This also allows for easier updates to category information without needing to update every product document. Brand information can also be referenced similarly to categories.

### 3️⃣ Graph Model *(Optional)*
In a graph model, we can represent the relationships between products, categories, users, and reviews as follows:

- Product, Category, User and Review can be nodes
- Relationship between product and category, and between product and reviews can be modelled using edges
- Moreover even the relationship between user and review can be modelled using edges

**“Products liked by people who reviewed similar products”**

- **Traversal**: 
  - Start at a product node, traverse to review nodes, then to user nodes, and finally to other product nodes that those users have reviewed. This allows us to find products that are liked by users who have shown interest in similar products.
