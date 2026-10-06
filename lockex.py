from redis_client import redis_client
import time

lock = redis_client.lock(
    "ticket_lock",
    timeout=10
)

with lock:

    print("Lock Acquired")

    time.sleep(5)

    print("Ticket Purchased")
