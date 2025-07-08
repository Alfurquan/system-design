## REST vs GraphQL

**Use REST if**
- Your API is simple and doesn’t require flexible queries.
- You need caching benefits from HTTP.
- You need a standardized, well-established API approach.
- You’re integrating with third-party services.
- Your team is already familiar with REST and need faster implementation.

**Use GraphQL if**
- You need flexible and efficient data fetching.
- Your API serves multiple clients (mobile, web, IoT) with different data needs.
- Real-time updates are required (GraphQL subscriptions).
- You want to avoid API versioning issues.
- Your application requires deeply nested data.

**Can You Use Both REST and GraphQL?**
- Absolutely! REST and GraphQL are not mutually exclusive, and many organizations implement a hybrid approach to get the best of both worlds:
- GraphQL for client-facing applications where flexibility, performance, and dynamic querying are essential.
- REST for admin interfaces, third-party integrations, and internal microservices where statelessness, caching, and simplicity are beneficial.

# **Problem Statement**
Design a backend for a Product Catalog Service to serve an e-commerce frontend (mobile + web). The frontend has the following needs:

- List of products with filtering, sorting, and pagination

- Product detail view showing:

    - Product info
    - Reviews
    - Seller info

- Authenticated access

- Rate limiting per client

You must implement both:

- A RESTful API using Flask

- A GraphQL API using Graphene

# API Implementation Plan

## A. REST API (with Flask)

### Endpoints

#### 1. `GET /products`
- **Description**: Fetch a list of products.
- **Supports**:
  - **Pagination**:
    - Query Params: `?page=1&limit=10`
  - **Filtering**:
    - Query Params: `?category=Electronics`
  - **Sorting**:
    - Query Params: `?sort_by=price&order=asc`

#### 2. `GET /products/<id>`
- **Description**: Returns a specific product's information including:
  - Product details
  - Associated reviews
  - Seller information

#### 3. `GET /sellers/<id>`
- **Description**: Returns information about the seller with the specified ID.

#### 4. `GET /products/<id>/reviews`
- **Description**: Returns all reviews associated with the given product ID.

### Additional Features

- **Token-based Authentication**:
  - Usage: `Authorization: Bearer <token>`
- **Rate Limiting**:
  - Restriction: 5 requests per minute per IP address

---

## B. GraphQL API (with Graphene)

### Queries to Support

```graphql
# 1. List products with optional pagination, filtering, and sorting
products(page: Int, limit: Int, category: String, sort_by: String, order: String): [Product]

# 2. Get detailed product information
product(id: ID!): Product {
  id
  name
  price
  reviews {
    rating
    comment
  }
  seller {
    name
  }
}
