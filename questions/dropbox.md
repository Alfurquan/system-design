# Dropbox like storage service

## Statement

Design a file storage service like dropbox

## Answer

1. **Functional requirements (Core requirements)**

    - Users should be able to upload a file
    - Users should be able to download a file
    - Users should be able to sync files
    - Users should be able to share files and view files shared with them

2. **Non functional requirements**

    - Availability >> Consistency
    - System should support large files (50 GB)
    - Fault tolerant
    - Low latency
    - Secure and reliable

3. **Core entities of the system**

    These will be the core entities of the system. We won't get into that much depth regarding columns and all now. Will discuss as we go along
    - **File:** This is the raw data that users will be uploading, downloading, and sharing.
    - **FileMetadata:** This is the metadata associated with the file. It will include information like the file's name, size, mime type, and the user  who uploaded it.
    - **User:** The user of our system.

4. **APIs**

    - Upload a file
        ```json
        POST /files
        {
            File,
            FileMetadata
        }
        ```

    - Download a file
        ```json
        GET /files/{fileId} -> File and FileMetadata
        ```

    - Share a file
        ```json
        POST /files/{fileId}/share
        {
            User[]
        }
        ```

    - View changes
        ```json
        GET /files/{fileId}/changes -> FileMetadata[]
        ```

5. **High level design**

    - **Users should be able to upload a file from any device**

        The main requirement for a system like Dropbox is to allow users to upload files. When it comes to storing a file, we need to consider two things:
        - Where do we store the file contents (the raw bytes)?
        - Where do we store the file metadata?

        For the file metadata, we can store it any noSQL DB like mongoDB or DynamoDB and this can be simple schema for the file metadata

        ```json
        {
             "id": "123",
            "name": "file.txt",
            "size": 1000,
            "mimeType": "text/plain",
            "uploadedBy": "user1"
        }
        ```

        For storing, files, we can upload them directly to blob storage like amazon S3 using pre-signed URLs.
        we can use presigned URLs to generate a URL that the user can use to upload the file directly to the Blob Storage service. Once the file is uploaded, the Blob Storage service will send a notification to our backend so we can save the metadata. . So whereas our initial API for upload was a POST to /files, it will now be a three step process:
        
        - Request a pre-signed URL from our backend (which itself gets the URL from the Blob Storage service like S3) and save the file metadata in our database with a status of "uploading."
        ```json
        POST /files/presigned-url -> PresignedUrl
        Request:
        {
          FileMetadata
        }
        ```
        
        - Use the presigned URL to upload the file to Blob Storage directly from the client. This is via a PUT request directly to the presigned URL where the file is the body of the request.

        - Once the file is uploaded, the Blob Storage service will send a notification to our backend using S3 Notifications. Our backend will then update the file metadata in our database with a status of "uploaded".
    
    - **Users should be able to download a file from any device**

        The best approach is to use a content delivery network (CDN) to cache the file closer to the user. A CDN is a network of servers distributed across the globe that cache files and serve them to users from the server closest to them. This reduces latency and speeds up download times.

        When a user requests a file, we can use the CDN to serve the file from the server closest to the user. This is much faster than serving the file from our backend or the Blob Storage service.

    - **Users should be able to share a file with other users**

         This would involve creating a new table that maps userId to fileId, where fileId is a file shared with the given user. This way, when a user opens our site, we can quickly get the list of files shared with them by querying the SharedFiles table for all of the files with a userId of the user.
        
    - **Users can automatically sync files across devices**

        We need to make sure that files are automatically synced across different devices. At a high level, this works by keeping a copy of a particular file on each client device (locally) and also in remote storage (i.e., the "cloud"). As such, there are two directions we need to sync in:
        - Local -> Remote
        - Remote -> Local

        **Local -> Remote**

        To do this, we need a client-side sync agent that:
        - Monitors the local Dropbox folder for changes using OS-specific file system events (like FileSystemWatcher on Windows or FSEvents on macOS)
        - When it detects a change, it queues the modified file for upload locally
        - It then uses our upload API to send the changes to the server along with updated metadata
        - Conflicts are resolved using a "last write wins" strategy - meaning if two users edit the same file, the most recent edit will be the one that's saved

        **Remote -> Local**

        For the other direction, each client needs to know when changes happen on the remote server so they can pull those changes down.
        There are two main approaches we could take:
        
        - Polling: The client periodically asks the server "has anything changed since my last sync?" The server would query the DB to see if any files that this user is watching has a updatedAt timestamp that is newer than the last time they synced. This is simple but can be slow to detect changes and wastes bandwidth if nothing has changed.
        
        - WebSocket or SSE: The server maintains an open connection with each client and pushes notifications when changes occur. This is more complex but provides real-time updates.

    - **Tying it all together**

        Here are the components of our design

        - Uploader: This is the client that uploads the file. It could be a web browser, a mobile app, or a desktop app. It is also responsible for proactively identifying local changes and pushing the updates to remote storage.
        
        - Downloader: This is the client that downloads the file. Of course, this can be the same client as the uploader, but it doesn't have to be. We separate them in our design for clarity. It is also responsible for determining when a file it has locally has changed on the remote server and downloading these changes.
        
        - LB & API Gateway: This is the load balancer and API Gateway that sits in front of our application servers. It's responsible for routing requests to the appropriate server and handling things like SSL termination, rate limiting, and request validation.
        
        - File Service: The file service is only responsible for writing to and from the file metadata db as well as requesting presigned URLs from S3. It doesn't actually handle the file upload or download. It's just a middleman between the client and S3.
        
        - File Metadata DB: This is where we store metadata about the files. This includes things like the file name, size, MIME type, and the user who uploaded the file. We also store a shared files table here that maps files to users who have access to them. We use this table to enforce permissions when a user tries to download a file.
        
        - S3: This is where the files are actually stored. We upload and download files directly to and from S3 using the presigned URLs we get from the file server.

        - CDN: This is a content delivery network that caches files close to the user to reduce latency. We use the CDN to serve files to the downloader.

6. **Potential deep dives**

    - **How can you support large files?**

      The first thing you should consider when thinking about large files is the user experience. There are two key insights that should stick out and ultimately guide your design:
      - Progress Indicator: Users should be able to see the progress of their upload so that they know it's working and how long it will take.
      - Resumable Uploads: Users should be able to pause and resume uploads. If they lose their internet connection or close the browser, they should be able to pick up where they left off rather than redownloading the 49GB that may have already been uploaded before the interruption.

      We can use a technique called "chunking" to break the file into smaller pieces and upload them one at a time (or in parallel, depending on network bandwidth). Chunking needs to be done on the client so that the file can be broken into pieces before it is sent to the server (or S3 in our case). A very common mistake candidates make is to chunk the file on the server, which effectively defeats the purpose since you still upload the entire file at once to get it on the server in the first place. When we chunk, we typically break the file into 5-10 MB pieces, but this can be adjusted based on the network conditions and the size of the file.

      With chunks, it's rather straightforward for us to show a progress indicator to the user. We can simply track the progress of each chunk and update the progress bar as each chunk is successfully uploaded. This provides a much better user experience than the user simply staring at a spinning wheel for an hour.

      The next question is: how will we handle resumable uploads? We need to keep track of which chunks have been uploaded and which haven't. We can do this by saving the state of the upload in the database, specifically in our FileMetadata table. Let's update the FileMetadata schema to include a chunks field.

      ```json
      {
        "id": "123",
        "name": "file.txt",
        "size": 1000,
        "mimeType": "text/plain",
        "uploadedBy": "user1",
        "status": "uploading",
        "chunks": [
          {
            "id": "chunk1",
            "status": "uploaded"
          },
          {
            "id": "chunk2",
            "status": "uploading"
          },
          {
            "id": "chunk3",
            "status": "not-uploaded"
          }
        ]
      }
      ```

      **But how should we ensure this chunks field is kept in sync with the actual chunks that have been uploaded?**

      A better approach is to use S3 event notifications to keep the chunks field in sync with the actual chunks that have been uploaded. S3 event notifications are a feature of S3 that allow you to trigger a Lambda function or send a message to an SNS topic when a file is uploaded to S3. We can use this feature to send a message to our backend when a chunk is successfully uploaded and then update the chunks field in the FileMetadata table without relying on the client.

      Taking a step back, we can tie it all together. Here is what will happen when a user uploads a large file:
      - The client will chunk the file into 5-10Mb pieces and calculate a fingerprint for each chunk. It will also calculate a fingerprint for the entire file, this becomes the fileId.
      
      - The client will send a GET request to fetch the FileMetadata for the file with the given fileId (fingerprint) in order to see if it already exists -- in which case, we can resume the upload.
      
      - If the file does not exist, the client will POST a request to /files/presigned-url to get a presigned URL for the file. The backend will save the file metadata in the FileMetadata table with a status of "uploading" and the chunks array will be a list of the chunk fingerprints with a status of "not-uploaded".
      
      - The client will then upload each chunk to S3 using the presigned URL. After each chunk is uploaded, S3 will send a message to our backend using S3 event notifications. Our backend will then update the chunks field in the FileMetadata table to mark the chunk as "uploaded".
      
      - Once all chunks in our chunks array are marked as "uploaded", the backend will update the FileMetadata table to mark the file as "uploaded".
            

    - **How can we make uploads, downloads, and syncing as fast as possible?**

      We can utilize compression to speed up both uploads and downloads. Compression reduces the size of the file, which means fewer bytes need to be transferred. We can compress a file on the client before uploading it and then decompress it on the server after it's uploaded. We can also compress the file on the server before sending it to the client and then rely on the client to decompress it.

    - **How can you ensure file security?**

      Security is a critical aspect of any file storage system. We need to ensure that files are secure and only accessible to authorized users.
      
      - Encryption in Transit: Sure, to most candidates, this is a no-brainer. We should use HTTPS to encrypt the data as it's transferred between the client and the server. This is a standard practice and is supported by all modern web browsers.
      
      - Encryption at Rest: We should also encrypt the files when they are stored in S3. This is a feature of S3 and is easy to enable. When a file is uploaded to S3, we can specify that it should be encrypted. S3 will then encrypt the file using a unique key and store the key separately from the file. This way, even if someone gains access to the file, they won't be able to decrypt it without the key. You can learn more about S3 encryption here.
      
      - Access Control: Our shareList or separate share table/cache is our basic ACL. As discussed earlier, we make sure that we share download links only with authorized users.
      
 


