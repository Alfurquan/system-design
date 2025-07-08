# Gopuff

## Statement

Design a backend system for Gopuff — where users can order items like snacks, groceries, and essentials and receive them in under 30 minutes from a nearby micro-fulfillment center.

## Answer

1. **Functional requirements (Core requirements)**

    - Customers should be able to query availability of items, deliverable in 1 hour, by location (i.e. the effective availability is the union of all inventory nearby DCs).
    - Customers should be able to order multiple items at the same time.
    
    **Below the line (out of scope)**
    - Handling payments/purchases.
    - Handling driver routing and deliveries.
    - Search functionality and catalog APIs. (The system is strictly concerned with availability and ordering).
    - Cancellations and returns.


2. **Non functional requirements**

    - Availability query < 100 ms latency
    - Ordering	Strongly consistent (no double-sell)
    - Fault tolerant
    - Scale - 10k DCs, 100k items, 10M orders/day
    - Secure and reliable

3. **Core entities of the system**

    Below will be the core entities of our system. We won't go into that much details, just lay out the entities for now
    - **Item**: A type of item, e.g. Cheetos. These are what our customers will actually care about.
    - **Inventory**: A physical instance of an item, located at a DC. We'll sum up Inventory to determine the quantity available to a specific user for a specific Item.
    - **Order**: A collection of Inventory which have been ordered by a user
    - **OrderItem**: Each item in the order.
    - **User**: The user of the system
    - **DistributionCenter**: A physical location where items are stored. We'll use these to determine which items are available to a user. Inventory are stored in DCs.

4. **APIs**

    - GET /v1/availability?lat=LAT&long=LONG&keyword={}&page_size={}&page_num={} ->
    { 
       items: {
         name: NAME
         quantity: QTY
       }[]
    }

    - POST /v1/order
    { 
      lat: LAT,
      long: LONG
      items: ITEM1,ITEM2,ITEM3...
      ...
    } -> Order | Failure

5. **High level design**

    - **Customers should be able to query availability of items**

    When a user makes a request to get availability for items A, B, and C from latitude X and longitude Y, here's what happens:
    
    - We make a request to the Availability Service with the user's location X and Y and any relevant filters.
    - The availability service fires a request to the Nearby Service with the user's location X and Y.
    - The nearby service returns us a list of DCs that can deliver to our location.
    - With the DCs available, the availability service query our database with those DC IDs.
    - We sum up the results and return them to our client.

    - **Customers should be able to order items.**

    By putting both orders and inventory in the same database, we can take advantage of the ACID properties of our Postgres database. Using a singular transaction with isolation level SERIALIZABLE we can ensure that the entire transaction is atomic. This means that if two users try to order the same item at the same time, one of them will be rejected. This is because the transaction will fail to commit if the inventory is not available.

    - The user makes a request to the Orders Service to place an order for items A, B, and C.
    
    - The Orders Service makes creates a singular transaction which we submit to our Postgres leader. This transaction: a. Checks the inventory for items A, B, and C > 0. b. If any of the items are out of stock, the transaction fails. c. If all items are in stock, the transaction records the order and updates the status for inventory items A, B, and C to "ordered". d. A new row is created in the Orders table (and OrderItems table) recording the order for A, B, and C. e. The transaction is committed.
    
    - If the transaction succeeds, we return the order to the user.
