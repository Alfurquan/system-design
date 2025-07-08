# API gateway

An API Gateway serves as a single entry point for all client requests, managing and routing them to appropriate backend services. Just as a hotel front desk handles check-ins, room assignments, and guest requests, an API Gateway manages centralized middleware like authentication, routing, and request handling.

## Core responsibilities

The gateway's primary function is request routing – determining which backend service should handle each incoming request. But this isn't all they do.

Nowadays, API gateways are also used to handle cross-cutting concerns or middleware like authentication, rate limiting, caching, SSL termination, and more.

## Tracing a Request

Let's walk through a request from start to finish. Incoming requests come into the API Gateway from clients, usually via HTTP but they can be gRPC or any other protocol. 

From there, the gateway will apply any middleware you've configured and then route the request to the appropriate backend service.

- Request validation
- API Gateway applies middleware (auth, rate limiting, etc.)
- API Gateway routes the request to the appropriate backend service
- Backend service processes the request and returns a response
- API Gateway transforms the response and returns it to the client
- Optionally cache the response for future requests