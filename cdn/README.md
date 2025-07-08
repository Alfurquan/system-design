# What is a CDN and when should you use it?

Modern systems often serve users globally, which makes it challenging to deliver content quickly to users all over the world. Users (and interviewers) expect fast load times, and delays can lead to a poor user experience and loss of traffic. A content delivery network (CDN) is a type of cache that uses distributed servers to deliver content to users based on their geographic location. CDNs are often used to deliver static content like images, videos, and HTML files, but they can also be used to deliver dynamic content like API responses.

They work by caching content on servers that are close to users. When a user requests content, the CDN routes the request to the closest server. If the content is cached on that server, the CDN will return the cached content. If the content is not cached on that server, the CDN will fetch the content from the origin server, cache it on the server, and then return the content to the user.

## Things you should know about CDNs

- **CDNs are not just for static assets:** While CDNs are often used to cache static assets like images, videos, and javascript files, they can also be used to cache dynamic content. This is especially useful for content that is accessed frequently, but changes infrequently. For example, a blog post that is updated once a day can be cached by a CDN.

- **CDNs can be used to cache API responses:** If you have an API that is accessed frequently, you can use a CDN to cache the responses. This can help reduce the load on your servers and improve the performance of your API.

- **Eviction policies:** Like other caches, CDNs have eviction policies that determine when cached content is removed. For example, you can set a time-to-live (TTL) for cached content, or you can use a cache invalidation mechanism to remove content from the cache when it changes.