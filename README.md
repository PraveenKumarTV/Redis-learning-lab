# Redis Learning Journey 🚀

This repository documents my hands-on Redis learning journey. The goal was not just to learn Redis commands, but to understand where Redis fits in real-world backend systems and how it solves performance and scalability problems.

---

# What is Redis?

Redis (Remote Dictionary Server) is an in-memory data store that is commonly used for:

- Caching
- Session Storage
- Rate Limiting
- Queues
- Pub/Sub Messaging
- Distributed Locks
- Leaderboards
- Event Streaming

Unlike traditional databases that primarily store data on disk, Redis keeps data in memory, making it extremely fast.

---

# Redis Setup

## Using Docker

```yaml
services:
  redis:
    image: redis:latest
    container_name: redis

    ports:
      - "6379:6379"
```

Start Redis:

```bash
docker compose up -d
```

Verify:

```bash
docker ps
```

Open Redis CLI:

```bash
docker exec -it redis redis-cli
```

---

# Basic Redis Commands

## Check Server Status

```bash
PING
```

Output:

```text
PONG
```

---

## Store Data

```bash
SET name Praveen
```

---

## Read Data

```bash
GET name
```

---

## Delete Data

```bash
DEL name
```

---

## Set Expiration

```bash
SET otp 1234 EX 60
```

---

## Check TTL

```bash
TTL otp
```

TTL = Time To Live.

Useful for:

- OTPs
- Sessions
- Temporary Cache

---

# Connecting Python to Redis

```python
import redis

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)
```

Store data:

```python
redis_client.set("course", "redis")
```

Read data:

```python
redis_client.get("course")
```

Delete data:

```python
redis_client.delete("course")
```

Store with expiration:

```python
redis_client.setex(
    "otp",
    60,
    "1234"
)
```

---

# Redis Caching

## Problem

Without cache:

```text
Client
   ↓
API
   ↓
Database
```

Every request hits the database.

---

## Solution

With Redis cache:

```text
Client
   ↓
API
   ↓
Redis
   ↓
Database (only if needed)
```

---

# Cache Hit

Data exists in Redis.

```text
Request
   ↓
Redis
   ↓
Data Found
   ↓
Response
```

---

# Cache Miss

Data does not exist in Redis.

```text
Request
   ↓
Redis
   ↓
Not Found
   ↓
Database
   ↓
Store in Redis
   ↓
Response
```

---

# Cache-Aside Pattern

Most common caching strategy.

```text
Request
   ↓
Redis
   ↓
Hit? → Return

Miss?
   ↓
Database
   ↓
Store in Redis
   ↓
Return
```

---

# Cache Invalidation

When data changes:

```text
Update Product
      ↓
Delete Cache
      ↓
Next Request Rebuilds Cache
```

Example:

```python
redis_client.delete("products:all")
redis_client.delete("product:1")
```

---

# Redis Sessions

## Purpose

Remember logged-in users.

---

## Login Flow

```text
User Login
    ↓
Create Session ID
    ↓
Store Session in Redis
```

Example:

```text
session:abc123
```

Value:

```json
{
  "id": 1,
  "username": "praveen"
}
```

---

## Benefits

Instead of querying the database on every request:

```text
Request
   ↓
Redis Session
   ↓
User Data
```

---

# Redis Rate Limiting

## Problem

Prevent API abuse.

```text
10000 requests
     ↓
Server Overload
```

---

## Solution

Store request count:

```text
rate:192.168.1.10
```

Increment:

```python
redis_client.incr(key)
```

Set expiration:

```python
redis_client.expire(key, 60)
```

Block after limit:

```text
Request 1 ✓
Request 2 ✓
Request 3 ✓
Request 4 ✓
Request 5 ✓
Request 6 ❌
```

---

# Redis Hashes

Store structured data.

Example:

```python
redis_client.hset(
    "user:1",
    mapping={
        "name": "Praveen",
        "role": "Admin",
        "city": "Chennai"
    }
)
```

Read:

```python
redis_client.hgetall("user:1")
```

Use Cases:

- User Profiles
- Settings
- Metadata

---

# Redis Lists (Queue)

## Purpose

Background job processing.

---

## Architecture

```text
API
 ↓
Redis Queue
 ↓
Worker
```

---

## Producer

```python
redis_client.lpush(
    "orders",
    job
)
```

---

## Consumer

```python
redis_client.brpop("orders")
```

---

## Use Cases

- Order Processing
- Email Sending
- Notifications
- Invoice Generation

---

# Redis Pub/Sub

## Purpose

Broadcast messages to multiple subscribers.

---

## Publisher

```python
redis_client.publish(
    "orders",
    "Order Created"
)
```

---

## Subscriber

```python
pubsub.subscribe("orders")
```

---

## Use Cases

- Notifications
- Live Updates
- Monitoring Events

---

# Queue vs Pub/Sub

## Queue

```text
Producer
   ↓
One Consumer
```

Only one worker receives the message.

---

## Pub/Sub

```text
Publisher
    ↓
Many Subscribers
```

All subscribers receive the message.

---

# Redis Sorted Sets

Store ranked data.

Example:

```python
redis_client.zadd(
    "leaderboard",
    {
        "Praveen": 500,
        "John": 700,
        "Alice": 300
    }
)
```

Get rankings:

```python
redis_client.zrevrange(
    "leaderboard",
    0,
    2,
    withscores=True
)
```

Use Cases:

- Leaderboards
- Trending Posts
- Most Viewed Content

---

# Distributed Locks

## Problem

Multiple processes modifying the same resource.

Example:

```text
1 Ticket Remaining

User A buys
User B buys
```

Without synchronization:

```text
Stock = -1
```

---

## Solution

Redis Lock

```python
lock = redis_client.lock(
    "ticket_lock"
)
```

Only one process enters the critical section.

---

## Use Cases

- Payments
- Inventory
- Ticket Booking
- Banking Systems

---

# Redis Streams

Redis Streams provide persistent event storage.

---

## Add Event

```python
redis_client.xadd(
    "orders",
    {
        "order_id": 101,
        "status": "created"
    }
)
```

---

## Read Events

```python
redis_client.xread(
    {"orders": "0"}
)
```

---

## Use Cases

- Event Processing
- Audit Logs
- Lightweight Event Streaming

---

# Queue vs Pub/Sub vs Streams

| Feature | Queue | Pub/Sub | Streams |
|----------|--------|----------|----------|
| Persistence | No | No | Yes |
| Multiple Consumers | Limited | Yes | Yes |
| Message History | No | No | Yes |
| Use Case | Jobs | Notifications | Event Streaming |

---

# Redis vs Kafka

| Feature | Redis | Kafka |
|----------|--------|--------|
| Cache | ✅ | ❌ |
| Sessions | ✅ | ❌ |
| Rate Limiting | ✅ | ❌ |
| Distributed Locks | ✅ | ❌ |
| Queue | ✅ | ✅ |
| Event Streaming | ⚠️ Streams | ✅ |
| Long-Term Storage | ❌ | ✅ |

---

# Most Common Redis Use Cases

1. Caching
2. Session Management
3. Rate Limiting
4. Background Jobs
5. Distributed Locks
6. Leaderboards
7. Notifications
8. Event Streaming

---

# Key Takeaways

- Redis is primarily an in-memory data store.
- The most common production use is caching.
- Sessions are often stored in Redis.
- Redis can implement rate limiting efficiently.
- Lists can be used as queues.
- Pub/Sub supports real-time notifications.
- Sorted Sets are ideal for rankings.
- Distributed Locks help coordinate concurrent operations.
- Redis Streams provide lightweight event streaming capabilities.
- Redis is often used alongside PostgreSQL or MongoDB, not as a replacement.

---

# Future Learning

- Redis Persistence (RDB & AOF)
- Redis Cluster
- Redis Sentinel
- Advanced Cache Strategies
- Redis Consumer Groups
- Redis + PostgreSQL
- Redis in Production Architectures

Happy Learning! 🚀
