# URL Shortening service

## Statement

 Design a URL Shortener System (like Bitly)

## Answer

1. **Functional requirements (Core requirements)**

- Users should be able to submit a long URL and receive a shortened version.
    -  Optionally, users should be able to specify a custom alias for their shortened URL.
    - Optionally, users should be able to specify an expiration date for their shortened URL.
- Users should be able to access the original URL by using the shortened URL.

2. **Non functional requirements**

- System must be highly available.
- System should be able to handle large amounts of load.
- The system should ensure uniqueness for the short codes (no two long URLs can map to the same short URL)
- The redirection should occur with minimal delay (< 100ms)

3. **Core entities of the system**

- Original URL: The original long URL that the user wants to shorten.
- Shortened URL: The shortened URL that the user receives and can share.
- User: Represents the user who created the shortened URL.

4. **APIs**

We will be using REST API's for the application.

- For shortening a URL we will need a POST endpoint

```json
POST /urls
{
  "long_url": "https://www.example.com/some/very/long/url",
  "custom_alias": "optional_custom_alias",
  "expiration_date": "optional_expiration_date"
}
->
{
  "short_url": "http://short.ly/abc123"
}
```

- For redirecting we will need a GET endpoint

```json
GET /{short_code}
-> HTTP 302 Redirect to the original long URL
```

5. **High level design**

- Users should be able to submit a long URL and receive a shortened version

    - Client: Users interact with the system through a web or mobile application.
    - Primary Server: The primary server receives requests from the client and handles all business logic like short url creation and validation.
    - Database: Stores the mapping of short codes to long urls, as well as user-generated aliases and expiration dates.

    When a user submits a long url, the client sends a POST request to /urls with the long url, custom alias, and expiration date. Then:

    - The Primary Server receives the request and validates the long URL. This is to ensure that the URL is valid (there's no point in shortening an invalid URL) and that it doesn't already exist in our system (we don't want collisions).
        - To validate that the URL is valid, we can use popular open-source libraries like is-url or write our own simple validation.
        - To check if the URL already exists in our system, we can query our database to see if the long URL is already present.
    - If the URL is valid and doesn't already exist, we can proceed to generate a short URL.

    - Once we have the short URL, we can proceed to insert it into our database, storing the short code (or custom alias), long URL, and expiration date.
    - Finally, we can return the short URL to the client.

- Users should be able to access the original URL by using the shortened URL

    When a user accesses a shortened URL, the following process occurs:
    - The user's browser sends a GET request to our server with the short code (e.g., GET /abc123).
    - Our Primary Server receives this request and looks up the short code (abc123) in the database.
    - If the short code is found and hasn't expired (by comparing the current date to the expiration date in the database), the server retrieves the corresponding long URL.
    - The server then sends an HTTP redirect response to the user's browser, instructing it to navigate to the original long URL.

    The response back to the client looks like this:

    ```json
    HTTP/1.1 302 Found
    Location: https://www.original-long-url.com
    ```

6. **Potential Deep Dives**

- How can we ensure short urls are unique?

    One way to guarantee we don't have collisions is to simply increment a counter for each new url. We can then take the output of the counter and encode it using base62 encoding to ensure it's a compacted representation.
    Redis is particularly well-suited for managing this counter because it's single-threaded and supports atomic operations. Being single-threaded means Redis processes one command at a time, eliminating race conditions. Its INCR command is atomic, meaning the increment operation is guaranteed to execute completely without interference from other operations. This is crucial for our counter - we need absolute certainty that each URL gets a unique number, with no duplicates or gaps.
    Each counter value is unique, eliminating the risk of collisions without the need for additional checks. Incrementing a counter and encoding it is computationally efficient, supporting high throughput. With proper counter management, the system can scale horizontally to handle massive numbers of URLs. The short code can be easily decoded back to the original ID if needed, aiding in database lookups.

- How can we ensure that redirects are fast?

    To improve redirect speed, we can introduce an in-memory cache like Redis or Memcached between the application server and the database. This cache stores the frequently accessed mappings of short codes to long URLs. When a redirect request comes in, the server first checks the cache. If the short code is found in the cache (a cache hit), the server retrieves the long URL from the cache, significantly reducing latency. If not found (a cache miss), the server queries the database, retrieves the long URL, and then stores it in the cache for future requests.

- How can we scale to support 1B shortened urls and 100M DAU?

    We'll start by looking at the size of our database.

    Each row in our database consists of a short code (~8 bytes), long URL (~100 bytes), creationTime (~8 bytes), optional custom alias (~100 bytes), and expiration date (~8 bytes). This totals to ~200 bytes per row. We can round up to 500 bytes to account for any additional metadata like the creator id, analytics id, etc.
    
    If we store 1B mappings, we're looking at 500 bytes * 1B rows = 500GB of data. The reality is, this is well within the capabilities of modern SSDs. Given the number of urls on the internet is our maximum bound, we can expect it to grow but only modestly. If we were to hit a hardware limit, we could always shard our data across multiple servers but a single Postgres instance, for example, should do for now.

    Coming back to our initial observation that reads are much more frequent than writes, we can scale our Primary Server by separating the read and write operations. This introduces a microservice architecture where the Read Service handles redirects while the Write service handles the creation of new short urls. This separation allows us to scale each service independently based on their specific demands.
    
    Now, we can horizontally scale both the Read Service and the Write Service to handle increased load. Horizontal scaling is the process of adding more instances of a service to distribute the load across multiple servers. This can help us handle a large number of requests per second without increasing the load on a single server. When a new request comes in, it is randomly routed to one of the instances of the service.

    Horizontally scaling our write service introduces a significant issue! For our short code generation to remain globally unique, we need a single source of truth for the counter. This counter needs to be accessible to all instances of the Write Service so that they can all agree on the next value.
    
    We could solve this by using a centralized Redis instance to store the counter. This Redis instance can be used to store the counter and any other metadata that needs to be shared across all instances of the Write Service. Redis is single-threaded and is very fast for this use case. It also supports atomic increment operations which allows us to increment the counter without any issues. Now, when a user requests to shorten a url, the Write Service will get the next counter value from the Redis instance, compute the short code, and store the mapping in the database.