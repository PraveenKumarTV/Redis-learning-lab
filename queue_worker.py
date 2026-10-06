import json
from redis_client import redis_client

print("Worker Started...")

while True:

    queue_name, job = redis_client.brpop("orders")

    order = json.loads(job)

    print("Processing Order")

    print(order)
