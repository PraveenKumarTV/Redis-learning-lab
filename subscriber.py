# subscriber.py

from redis_client import redis_client

pubsub = redis_client.pubsub()

pubsub.subscribe("orders")

print("Listening...")

for message in pubsub.listen():

    if message["type"] == "message":

        print(message["data"])
