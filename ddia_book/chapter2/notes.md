# Chapter 2: Data Models and Query Languages

## Relational model vs Document model

**Relational model**
- Data is organized into relations (called tables in SQL)
- Each relation is an unordered collection of tuples (rows in SQL).

**NoSQL**

There are several driving forces behind the adoption of NoSQL databases, including:
- A need for greater scalability than relational databases can easily achieve, includ‐
ing very large datasets or very high write throughput
- A widespread preference for free and open source software over commercial
database products
- Specialized query operations that are not well supported by the relational model
- Frustration with the restrictiveness of relational schemas, and a desire for a more
dynamic and expressive data model 

Representing a LinkedIn profile as a JSON document

```json
{
 "user_id": 251,
 "first_name": "Bill",
 "last_name": "Gates",
 "summary": "Co-chair of the Bill & Melinda Gates... Active blogger.",
 "region_id": "us:91",
 "industry_id": 131,
 "photo_url": "/p/7/000/253/05b/308dd6e.jpg",
 "positions": [
 {"job_title": "Co-chair", "organization": "Bill & Melinda Gates Foundation"},
 {"job_title": "Co-founder, Chairman", "organization": "Microsoft"}
 ],
 "education": [
 {"school_name": "Harvard University", "start": 1973, "end": 1975},
 {"school_name": "Lakeside School, Seattle", "start": null, "end": null}
 ],
 "contact_info": {
 "blog": "http://thegatesnotes.com",
 "twitter": "http://twitter.com/BillGates"
 }
}
```
The JSON representation has better locality than the multi-table schema. If you want to fetch a profile in the relational example, you need to either
perform multiple queries (query each table by user_id) or perform a messy multiway join between the users table and its subordinate tables. In the JSON representa‐tion, all the relevant information is in one place, and one query is sufficient.

The one-to-many relationships from the user profile to the user’s positions, educational history, and contact information imply a tree structure in the data, and the JSON representation makes this tree structure explicit 

The main arguments in favor of the document data model are schema flexibility, better performance due to locality, and that for some applications it is closer to the data structures used by the application. The relational model counters by providing better support for joins, and many-to-one and many-to-many relationships.

**Which data model leads to simpler application code?**

If the data in your application has a document-like structure (i.e., a tree of one-tomany relationships, where typically the entire tree is loaded at once), then it’s probably a good idea to use a document model. The relational technique of shredding— splitting a document-like structure into multiple tables (like positions, education, and contact_info)—can lead to cumbersome schemas and unnecessarily complicated application code.

**Schema flexibility in the document model**
Document databases are sometimes called schemaless, but that’s misleading, as the
code that reads the data usually assumes some kind of structure—i.e., there is an
implicit schema, but it is not enforced by the database. A more accurate term is
schema-on-read (the structure of the data is implicit, and only interpreted when the
data is read), in contrast with schema-on-write (the traditional approach of relational databases, 
where the schema is explicit and the database ensures all written data conforms to it)

The difference between the approaches is particularly noticeable in situations where
an application wants to change the format of its data. For example, say you are cur‐
rently storing each user’s full name in one field, and you instead want to store the
first name and last name separately. In a document database, you would just
start writing new documents with the new fields and have code in the application that
handles the case when old documents are read

## Query language for data

**Imperative vs Declarative**
- An imperative language tells the computer to perform certain operations in a certain
order. You can imagine stepping through the code line by line, evaluating conditions,
updating variables, and deciding whether to go around the loop one more time.

- In a declarative query language, like SQL or relational algebra, you just specify the
pattern of the data you want—what conditions the results must meet, and how you
want the data to be transformed (e.g., sorted, grouped, and aggregated)—but not how
to achieve that goal. It is up to the database system’s query optimizer to decide which
indexes and which join methods to use, and in which order to execute various parts
of the query.

- Declarative languages often lend themselves to parallel execution

- Imperative code is very hard to parallelize across mul‐
tiple cores and multiple machines, because it specifies instructions that must be per‐
formed in a particular order. Declarative languages have a better chance of getting
faster in parallel execution because they specify only the pattern of the results, not the
algorithm that is used to determine the results. The database is free to use a parallel
implementation of the query language, if appropriate.

**Map Reduce querying**

MapReduce is a programming model for processing large amounts of data in bulk
across many machines, popularized by Google.

MapReduce is neither a declarative query language nor a fully imperative query API,
but somewhere in between: the logic of the query is expressed with snippets of code,
which are called repeatedly by the processing framework. It is based on the map (also
known as collect) and reduce (also known as fold or inject) functions that exist
in many functional programming languages.

## Graph like data models
If your application has mostly one-to-many rela‐
tionships (tree-structured data) or no relationships between records, the document
model is appropriate.

But what if many-to-many relationships are very common in your data? The relational model can handle simple cases of many-to-many relationships, but as the connections within your data become more complex, it becomes more natural to start
modeling your data as a graph.

A graph consists of two kinds of objects: vertices (also known as nodes or entities) and
edges (also known as relationships or arcs). Many kinds of data can be modeled as a
graph. Typical examples include:
- Social graphs: Vertices are people, and edges indicate which people know each other.

- The web graph: Vertices are web pages, and edges indicate HTML links to other pages.

- Road or rail networks: Vertices are junctions, and edges represent the roads or railway lines between
them.

### Property graph model

In the property graph model, each vertex consists of:
- A unique identifier
- A set of outgoing edges
- A set of incoming edges
- A collection of properties

Each edge consists of:
- A unique identifier
- The vertex at which the edge starts (the tail vertex)
- The vertex at which the edge ends (the head vertex)
- A label to describe the kind of relationship between the two vertices
- A collection of properties (key-value pairs)

**Representing a property graph using a relational schema**
```SQL
CREATE TABLE vertices (
 vertex_id integer PRIMARY KEY,
 properties json
);
CREATE TABLE edges (
 edge_id integer PRIMARY KEY,
 tail_vertex integer REFERENCES vertices (vertex_id),
 head_vertex integer REFERENCES vertices (vertex_id),
 label text,
 properties json
);
CREATE INDEX edges_tails ON edges (tail_vertex);
CREATE INDEX edges_heads ON edges (head_vertex);
```

### The cypher query language
Cypher is a declarative query language for property graphs, created for the Neo4j
graph database

# 📦 Data Model Considerations

| Factor                  | Relational            | Document                  | Graph                        |
|-------------------------|------------------------|-----------------------------|-------------------------------|
| **Flexibility**         | Low                    | High                        | Medium                        |
| **Join Support**        | Strong                 | Weak                        | Native traversal              |
| **Horizontal Scalability** | Challenging         | Easier                      | Difficult                     |
| **Best For**            | OLAP, structured data  | Aggregates, semi-structured| Relationships, social graphs  |

---

# ⚖️ Trade-offs Cheat Sheet

| Trade-off Area          | Relational             | Document                   | Graph                         |
|--------------------------|------------------------|------------------------------|-------------------------------|
| **Schema evolution**     | Painful                | Easy                        | Medium                        |
| **Redundancy**           | Avoided via joins      | Encouraged for locality     | Avoided, stored in edges      |
| **Consistency**          | Easy via constraints   | Hard if duplicated data     | Easy with strong semantics    |
| **Query complexity**     | Simple queries + joins | Nested fields, few joins    | Traversals, recursive queries |
| **Tooling**              | Mature                 | Varies by DB                | Limited                       |
