# Pastebin

## Statement

Design Pastebin — a system where users can paste text and share it.

1. **Functional requirements (Core requirements)**
    - Users should be able to paste text and get a link back to share
    - Users should be able to access text using the link
    - Optional: Users should be able to specify expiry for the link

2. **Non functional requirements**

    - Availability >> Consistency
    - Fault tolerant
    - Low latency
    - Secure and reliable

3. **Core entities of the system**
    These will be the core entities of the system.

    - Paste: The piece of text user paste in.
    - PasteMetadata: The metadata for the piece of text, like pasteId, expiryTime, createdBy, size etc
    - User: The user of the system

4. **APIs**

    - Upload a paste
        ```json
        POST /pastes
        {
          paste: string,
          expiryTime?: string,   // e.g. "1h", "1d"
        }
        ```
        Response
        ```json
        201 Created
        {
          "pasteId": "abc123",
          "url": "https://pastebin.com/abc123"
        }
        ```

    - Access a paste
        ```json
        GET /pastes/{pasteId}
        ```
        Response
        ```json
        200 OK
        {
          "paste": "text content here",
          "createdAt": "2025-07-02T10:00:00Z",
          "expiryTime": "2025-07-03T10:00:00Z"
        }
        ```
5. **High level design**

    - **Users should be able to upload a paste**

        The main requirement for a system like pastebin is to allow users to upload pastes. When it comes to storing a paste, we need to consider two things:
        - Where do we store the paste contents (the raw bytes)?
        - Where do we store the paste metadata?

        For the paste metadata, we can store it any noSQL DB like mongoDB or DynamoDB and this can be simple schema for the paste metadata

        ```json
        {
            "id": "123",
            "mimeType": "text/plain",
            "expiryTime": "Wed 22 July, 12 pm",
            "uploadedBy": "user1"
        }
        ```

        For storing, pastes, we can upload them directly to blob storage like amazon S3 using pre-signed URLs.
        we can use presigned URLs to generate a URL that the user can use to upload the paste directly to the Blob Storage service. Once the paste is uploaded, the Blob Storage service will send a notification to our backend so we can save the metadata. So whereas our initial API for upload was a POST to /pastes, it will now be a three step process:
        
        - Request a pre-signed URL from our backend (which itself gets the URL from the Blob Storage service like S3) and save the paste metadata in our database with a status of "uploading."
        ```json
        POST /pastes/presigned-url -> PresignedUrl
        Request:
         {
          paste: string,
          expiryTime?: string,   // e.g. "1h", "1d"
        }
        ```
        
        - Use the presigned URL to upload the paste to Blob Storage directly from the client. This is via a PUT request directly to the presigned URL where the paste is the body of the request.

        - Once the paste is uploaded, the Blob Storage service will send a notification to our backend using S3 Notifications. Our backend will then update the paste metadata in our database with a status of "uploaded".
    
    - **Users should be able to view the paste**

        The best approach is to use a content delivery network (CDN) to cache the paste closer to the user. A CDN is a network of servers distributed across the globe that cache pastes and serve them to users from the server closest to them. This reduces latency and speeds up download times.

        When a user requests a paste, we can use the CDN to serve the paste from the server closest to the user. This is much faster than serving the paste from our backend or the Blob Storage service.

6. **Potential deep dives**

    - What if the client uploads to blob but the notification fails? How will you clean up "orphaned" pastes in blob storage?
      When the client uploads a paste, first we will store paste metadata in the database with the status as uploading. After that we will generate a presigned URL and send it back to the client. 
      The client will then use the pre signed URL to upload the paste to blob. Once the upload succeeds, blob will send a notification to our server and we will update the status of the paste metadata in the database to uploaded.

      Now, coming to the question,
      when notification fails, the status of the paste in the database will be uploading. We can use a scheduled job in our server to periodically cleanup orphaned pastes in blob storage, The job will check the status field in the database and if the status is not uploaded and paste is present in blob, it will clean it up.

    - What if the metadata write to DB fails but the blob upload succeeds?
      Going by above approach if metadata write to DB fails, we will first of all not send any pre signed URLs to the client and instead send them a 500 error. So there will be no untracked blobs in blob storage.

    - Do you cache metadata too?
      Yes we can have a cache layer like redis or memcached to cache metadata to allow faster lookups.

    - What TTL mechanism will you use?
      We can use the CDN expiration rules here
        
