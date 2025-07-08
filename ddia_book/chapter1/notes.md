# Chapter 1: Reliable, Scalable, and Maintainable Applications

## Three important concepts

- **Reliability**: The system should continue to work correctly (performing the correct function at
the desired level of performance) even in the face of adversity (hardware or soft‐
ware faults, and even human error). 

- **Scalability**: As the system grows (in data volume, traffic volume, or complexity), there should
be reasonable ways of dealing with that growth.

- **Maintainability**: Over time, many different people will work on the system (engineering and oper‐
ations, both maintaining current behavior and adapting the system to new use
cases), and they should all be able to work on it productively. 

## How Important Is Reliability?
Reliability is not just for nuclear power stations and air traffic control software—
more mundane applications are also expected to work reliably. Bugs in business
applications cause lost productivity (and legal risks if figures are reported incor‐
rectly), and outages of ecommerce sites can have huge costs in terms of lost revenue
and damage to reputation.

## Scalability

### Latency and response time
Latency and response time are often used synonymously, but they
are not the same. The response time is what the client sees: besides
the actual time to process the request (the service time), it includes
network delays and queueing delays. Latency is the duration that a
request is waiting to be handled—during which it is latent, await‐
ing service
