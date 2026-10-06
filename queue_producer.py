import json
from redis_client import redis_client

job = {
    "order_id": 101,
    "customer": "Praveen",
    "amount": 500
}

redis_client.lpush(
    "orders",
    json.dumps(job)
)

print("Job Added")
