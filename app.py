from redis_client import redis_client

redis_client.set("user_id",101);
redis_client.set("username","praveen");
redis_client.set("email","praveen@gmail.com")

print(redis_client.get("username"))
