# Transactions

A transaction is a way for an application to group several reads and writes
together into a logical unit. Conceptually, all the reads and writes in a transaction are
executed as one operation: either the entire transaction succeeds (commit) or it fails
(abort, rollback). If it fails, the application can safely retry. With transactions, error
handling becomes much simpler for an application, because it doesn’t need to worry
about partial failure—i.e., the case where some operations succeed and some fail (for
whatever reason).

## The Meaning of ACID

The safety guarantees provided by transactions are often described by the wellknown acronym ACID, which stands for Atomicity, Consistency, Isolation, and Durability. 

### Atomicity

In general, atomic refers to something that cannot be broken down into smaller parts. For example, in multi-threaded programming, if one thread executes an atomic operation, that means there is no way that another thread could see the half-finished
result of the operation. The system can only be in the state it was before the operation
or after the operation, not something in between.

ACID atomicity describes what happens if a client wants to make several
writes, but a fault occurs after some of the writes have been processed—for example,
a process crashes, a network connection is interrupted, a disk becomes full, or some
integrity constraint is violated. If the writes are grouped together into an atomic
transaction, and the transaction cannot be completed (committed) due to a fault, then
the transaction is aborted and the database must discard or undo any writes it has
made so far in that transaction.

### Consistency

The idea of ACID consistency is that you have certain statements about your data
(invariants) that must always be true—for example, in an accounting system, credits
and debits across all accounts must always be balanced. If a transaction starts with a
database that is valid according to these invariants, and any writes during the transac‐
tion preserve the validity, then you can be sure that the invariants are always satisfied.

Atomicity, isolation, and durability are properties of the database, whereas consis‐
tency (in the ACID sense) is a property of the application. The application may rely
on the database’s atomicity and isolation properties in order to achieve consistency,
but it’s not up to the database alone. Thus, the letter C doesn’t really belong in ACID.

### Isolation

Most databases are accessed by several clients at the same time. That is no problem if
they are reading and writing different parts of the database, but if they are accessing
the same database records, you can run into concurrency problems.

Isolation in the sense of ACID means that concurrently executing transactions are
isolated from each other: they cannot step on each other’s toes. The classic database
textbooks formalize isolation as serializability, which means that each transaction can
pretend that it is the only transaction running on the entire database. The database
ensures that when the transactions have committed, the result is the same as if they
had run serially (one after another), even though in reality they may have run con‐
currently

### Durability

The purpose of a database system is to provide a safe place where data can be stored
without fear of losing it. Durability is the promise that once a transaction has com‐
mitted successfully, any data it has written will not be forgotten, even if there is a
hardware fault or the database crashes.


## Single-Object and Multi-Object Operations

Multi-object transactions require some way of determining which read and write
operations belong to the same transaction. In relational databases, that is typically
done based on the client’s TCP connection to the database server: on any particular
connection, everything between a BEGIN TRANSACTION and a COMMIT statement is
considered to be part of the same transaction.

### Single-object writes

Atomicity and isolation also apply when a single object is being changed. For exam‐
ple, imagine you are writing a 20 KB JSON document to a database:
- If the network connection is interrupted after the first 10 KB have been sent, does
the database store that unparseable 10 KB fragment of JSON?
- If the power fails while the database is in the middle of overwriting the previous
value on disk, do you end up with the old and new values spliced together?
- If another client reads that document while the write is in progress, will it see a
partially updated value?

Those issues would be incredibly confusing, so storage engines almost universally
aim to provide atomicity and isolation on the level of a single object (such as a keyvalue pair) on one node

### The need for multi-object transactions

There are some use cases in which single-object inserts, updates, and deletes are suffi‐
cient. However, in many other cases writes to several different objects need to be
coordinated:
- In a relational data model, a row in one table often has a foreign key reference to
a row in another table. (Similarly, in a graph-like data model, a vertex has edges
to other vertices.) Multi-object transactions allow you to ensure that these refer‐
ences remain valid: when inserting several records that refer to one another, the
foreign keys have to be correct and up to date, or the data becomes nonsensical.
- In a document data model, the fields that need to be updated together are often
within the same document, which is treated as a single object—no multi-object
transactions are needed when updating a single document. However, document
databases lacking join functionality also encourage denormalization (see “Rela‐
tional Versus Document Databases Today” on page 38). When denormalized
information needs to be updated, like in the example of Figure 7-2, you need to
update several documents in one go. Transactions are very useful in this situation
to prevent denormalized data from going out of sync.
- In databases with secondary indexes (almost everything except pure key-value
stores), the indexes also need to be updated every time you change a value. These
indexes are different database objects from a transaction point of view: for exam‐
ple, without transaction isolation, it’s possible for a record to appear in one index
but not another, because the update to the second index hasn’t happened yet.

## Weak Isolation Levels

If two transactions don’t touch the same data, they can safely be run in parallel,
because neither depends on the other. Concurrency issues (race conditions) only
come into play when one transaction reads data that is concurrently modified by
another transaction, or when two transactions try to simultaneously modify the same
data.

### Read Committed

The most basic level of transaction isolation is read committed.
It makes two guaran‐tees:
- When reading from the database, you will only see data that has been committed
(no dirty reads).
- When writing to the database, you will only overwrite data that has been com‐
mitted (no dirty writes).

#### No dirty reads

Imagine a transaction has written some data to the database, but the transaction has
not yet committed or aborted. Can another transaction see that uncommitted data? If
yes, that is called a dirty read.

Transactions running at the read committed isolation level must prevent dirty reads.
This means that any writes by a transaction only become visible to others when that
transaction commits 

#### No dirty writes

What happens if two transactions concurrently try to update the same object in a
database? We don’t know in which order the writes will happen, but we normally
assume that the later write overwrites the earlier write.
However, what happens if the earlier write is part of a transaction that has not yet
committed, so the later write overwrites an uncommitted value? This is called a dirty
write. 
Transactions running at the read committed isolation level must prevent
dirty writes, usually by delaying the second write until the first write’s transaction has
committed or aborted.

#### Implementing read committed

**Dirty writes**

Most commonly, databases prevent dirty writes by using row-level locks: when a
transaction wants to modify a particular object (row or document), it must first
acquire a lock on that object. It must then hold that lock until the transaction is com‐
mitted or aborted. Only one transaction can hold the lock for any given object; if
another transaction wants to write to the same object, it must wait until the first
transaction is committed or aborted before it can acquire the lock and continue.

**Dirty reads**

For every object that is written, the database remembers both the old com‐
mitted value and the new value set by the transaction that currently holds the write
lock. While the transaction is ongoing, any other transactions that read the object are
simply given the old value. Only when the new value is committed do transactions
switch over to reading the new value. 

### Snapshot Isolation and Repeatable Read





