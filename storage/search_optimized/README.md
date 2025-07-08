# What is a search optimized database and when should you use it?

Sometimes you're tasked with implementing full-text search as a feature of your design. Full-text search is the ability to search through a large amount of text data and find relevant results. This is different from a traditional database query, which is usually based on exact matches or ranges. Without a search optimized database, you would need to run a query that looks something like this:

```sql
SELECT * FROM documents WHERE document_text LIKE '%search_term%'
```

This query is slow and inefficient, and it doesn't scale well because it requires a full table scan.

Search optimized databases, on the other hand, are specifically designed to handle full-text search. They use techniques like indexing, tokenization, and stemming to make search queries fast and efficient. In short, they work by building what are called inverted indexes. Inverted indexes are a data structure that maps from words to the documents that contain them. This allows you to quickly find documents that contain a given word.

A simple example of an inverted index might look like this:

```json
{
  "word1": [doc1, doc2, doc3],
  "word2": [doc2, doc3, doc4],
  "word3": [doc1, doc3, doc4]
}
```

Now, instead of scanning the entire table, the database can quickly look up the word in the query and find all the matching documents. Fast!

**Where to use it**

Examples of search optimized databases are straightforward, consider an application like Ticketmaster that needs to search through a large number of events to find relevant results. Or a social media platform like Twitter that needs to search through a large number of tweets to find relevant results. In either case, a search optimized database would be an optimal choice.

## Things you should know about search optimized databases

- **Inverted Indexes:** As just mentioned, search optimized databases use inverted indexes to make search queries fast and efficient. An inverted index is a data structure that maps from words to the documents that contain them. This allows you to quickly find documents that contain a given word.

- **Tokenization:** Tokenization is the process of breaking a piece of text into individual words. This allows you to map from words to documents in the inverted index.

- **Stemming:** Stemming is the process of reducing words to their root form. This allows you to match different forms of the same word. For example, "running" and "runs" would both be reduced to "run".

- **Fuzzy Search:** Fuzzy search is the ability to find results that are similar to a given search term. Most search optimized databases support fuzzy search out of the box as a configuration option. In short, this works by using algorithms that can tolerate slight misspellings or variations in the search term. This is achieved through techniques like edit distance calculation, which measures how many letters need to be changed, added, or removed to transform one word into another.

- **Scaling:** Just like traditional databases, search optimized databases scale by adding more nodes to a cluster and sharding data across those nodes.