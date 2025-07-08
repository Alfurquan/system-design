# What is blob storage and when should you use it?

Sometimes you'll need to store large, unstructured blobs of data. This could be images, videos, or other files. Storing these large blobs in a traditional database is both expensive and inefficient and should be avoided when possible. Instead, you should use a blob storage service like Amazon S3 or Google Cloud Storage. These platforms are specifically designed for handling large blobs of data, and are much more cost effective than a traditional database.

Blob storage services are simple. You can upload a blob of data and that data is stored and get back a URL. You can then use this URL to download the blob of data. Often times blob storage services work in conjunction with CDNs, so you can get fast downloads from anywhere in the world. Upload a file/blob to blob storage which will act as your origin, and then use a CDN to cache the file/blob in edge locations around the world.

Avoid using blob storage like S3 as your primary database unless you have a very good reason. In a typical setup you will have a core database like Postgres or DynamoDB that has pointers (just a url) to the blobs stored in S3. This allows you to use the database to query and index the data with very low latency, while still getting the benefits of cheap blob storage.

Here are some common examples of when to use blob storage:

- **Design Youtube:** Store videos in blob storage, store metadata in a database.
- **Design Instagram:** Store images & videos in blob storage, store metadata in a database.
- **Design Dropbox:** Store files in blob storage, store metadata in a database.


To upload:
- When clients want to upload a file, they request a presigned URL from the server.
- The server returns a presigned URL to the client, recording it in the database.
- The client uploads the file to the presigned URL.
- The blob storage triggers a notification to the server that the upload is complete and the status is updated.

To download:
- The client requests a specific file from the server and are returned a presigned URL.
- The client uses the presigned URL to download the file via the CDN, which proxies the request to the underlying blob storage.


## Things you should know about blob storage

- **Durability:** Blob storage services are designed to be incredibly durable. They use techniques like replication and erasure coding to ensure that your data is safe even if a disk or server fails.

- **Scalability:** Hosted blob storage solutions like AWS S3 can be considered infinitely scalable. They can store an unlimited amount of data and can handle an unlimited number of requests (obviously within the limits of your account). As a result, in your interview, you don't need to explicitly consider the scalability of blob storage services -- consider this as a given.

- **Cost:** Blob storage services are designed to be cost effective. They are much cheaper than storing large blobs of data in a traditional database. For example, AWS S3 charges $0.023 per GB per month for the first 50 TB of storage. This is much cheaper than storing the same data in a database like DynamoDB, which charges $1.25 per GB per month for the first 10 TB of storage.

- **Security:** Blob storage services have built-in security features like encryption at rest and in transit. They also have access control features that allow you to control who can access your data.

- **Upload and Download Directly from the Client:** Blob storage services allow you to upload and download blobs directly from the client. This is useful for applications that need to store and retrieve large blobs of data, like images or videos. Familiarize yourself with presigned URLs and how they can be used to grant temporary access to a blob -- either for upload or download.

- **Chunking:** When uploading large files, it's common to use chunking to upload the file in smaller pieces. This allows you to resume an upload if it fails partway through, and it also allows you to upload the file in parallel. This is especially useful for large files, where uploading the entire file at once might take a long time. Modern blob storage services like S3 support chunking out of the box via the multipart upload API.

- **Flat namespace**: Quick file lookups

- **Immutable writes**: No locks or races

- **Redundancy**: Durable data

## What should we know for interviews

- Metadata in traditional database and large files in object storage
- We can upload directly using pre signed URLs
- Large files are uploaded in chunks and then we can stitch them together.