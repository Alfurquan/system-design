# Websockets: Real-Time Bidirectional Communication

## Overview

WebSockets provide a persistent, TCP-style connection between client and server, allowing for real-time, bidirectional communication with broad support (including browsers). Unlike HTTP's request-response model, WebSockets enable servers to push data to clients without being prompted by a new request. Similarly clients can push data back to the server without the same wait.

Unlike the traditional HTTP protocol, where the client sends a request to the server and waits for a response, WebSockets allow both the client and server to send messages to each other independently and continuously after the connection is established.

## How do they work ?

The WebSocket connection starts with a standard HTTP request from the client to the server.

However, instead of completing the request and closing the connection, the server responds with an HTTP 101 status code, indicating that the protocol is switching to WebSockets.

After this handshake, a WebSocket connection is established, and both the client and server can send messages to each other over the open connection.

### Step by step process

- **Handshake:** The client initiates a connection request using a standard HTTP GET request with an "Upgrade" header set to "websocket". If the server supports WebSockets and accepts the request, it responds with a special 101 status code, indicating that the protocol will be changed to WebSocket.

- **Connection:** Once the handshake is complete, the WebSocket connection is established. This connection remains open until explicitly closed by either the client or the server.

- **Data transfer:** Both the client and server can now send and receive messages in real-time. These messages are sent in small packets called frames, and carry minimal overhead compared to traditional HTTP requests.

- **Closure:** The connection can be closed at any time by either the client or server, typically with a "close" frame indicating the reason for closure.

### Why are they used ?

WebSockets offer several advantages that make them ideal for certain types of applications:

- **Real-time Updates:** WebSockets enable instant data transmission, making them perfect for applications that require real-time updates, like live chat, gaming, or financial trading platforms.

- **Reduced Latency:** Since the connection is persistent, there's no need to establish a new connection for each message, significantly reducing latency.

- **Efficient Resource Usage:** WebSockets are more efficient than traditional polling techniques, as they don't require the client to continuously ask the server for updates.

- **Bidirectional Communication:** Both the client and server can initiate communication, allowing for more dynamic and interactive applications.

- **Lower Overhead:** After the initial handshake, WebSocket frames have a small header (as little as 2 bytes), reducing the amount of data transferred.

### Where are they used ?

- **Real-Time Collaboration Tools:** Applications like Google Docs may use WebSockets to enable multiple users to edit a document simultaneously. Changes made by one user are instantly reflected for all others, creating a seamless collaborative experience.

- **Real-Time Chat Applications:**One of the most popular uses of WebSockets is in real-time chat applications.Messaging platforms like Slack use WebSockets to deliver messages instantly. This allows for real-time conversations and immediate message delivery notifications.

- **Live Notifications:** Social media platforms use WebSockets to push real-time notifications to users when they receive a new message, like, or comment. Instead of the client constantly checking for new notifications, the server can push updates to the client as soon as they occur.

- **Multiplayer Online Games:** In online multiplayer games, low latency is crucial for a seamless gaming experience. WebSockets provide the necessary real-time communication between the game server and players, ensuring that all players see the same game state simultaneously.

- **Financial Market Data Feeds:** WebSockets are widely used in financial applications to stream real-time market data, such as stock prices, forex rates, and cryptocurrency values.

- **IoT (Internet of Things) Applications:** In IoT applications, devices often need to communicate with a server in real time. WebSockets provide a lightweight and efficient communication channel for sending sensor data, receiving commands, and synchronizing device states.

- **Live Streaming and Broadcasting:** While the actual video streaming typically uses other protocols, WebSockets can be used for real-time chat, viewer counts, and other interactive features during live broadcasts

