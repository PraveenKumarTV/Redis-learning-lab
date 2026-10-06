# publisher.py

from redis_client import redis_client

redis_client.publish(
    "orders",
    "Order 101 Created"
)

print("Published")
