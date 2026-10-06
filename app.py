from flask import Flask, request
import uuid
import json
import time

from redis_client import redis_client

app = Flask(__name__)

products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 50000
    },
    {
        "id": 2,
        "name": "Phone",
        "price": 25000
    },
    {
        "id": 3,
        "name": "Keyboard",
        "price": 1000
    }
]

users = [
    {
        "id": 1,
        "username": "praveen",
        "password": "123"
    },
    {
        "id": 2,
        "username": "john",
        "password": "456"
    }
]

@app.get("/products")
def get_products():
    return products

@app.get("/products/<int:product_id>")
def get_product(product_id):

    cache_key = f"product:{product_id}"

    cached_product = redis_client.get(cache_key)

    if cached_product:

        print("CACHE HIT")
        try:
            return json.loads(cached_product)
        except json.JSONDecodeError:
            print("Cache corrupted - Treating as MISS")
            redis_client.delete(cache_key)

    print("CACHE MISS")

    time.sleep(5)

    for product in products:

        if product["id"] == product_id:

            redis_client.setex(
                cache_key,
                600,
                json.dumps(product)
            )

            return product

    return {"error": "Product not found"}, 404

@app.put("/products/<int:product_id>")
def update_product(product_id):

    for product in products:

        if product["id"] == product_id:

            product["price"] = 99999

            return {
                "message": "updated",
                "product": product
            }

    return {"error": "not found"}, 404


@app.post("/login")
def login():

    data = request.json

    username = data["username"]
    password = data["password"]

    for user in users:

        if (
            user["username"] == username
            and user["password"] == password
        ):

            session_id = str(uuid.uuid4())

            redis_client.setex(
                f"session:{session_id}",
                3600,
                json.dumps(user)
            )

            return {
                "message": "login successful",
                "session_id": session_id
            }

    return {
        "message": "invalid credentials"
    }, 401

@app.get("/profile")
def profile():

    session_id = request.headers.get(
        "Session-Id"
    )

    if not session_id:

        return {
            "message": "session missing"
        }, 401

    user = redis_client.get(
        f"session:{session_id}"
    )

    if not user:

        return {
            "message": "invalid session"
        }, 401

    return json.loads(user)

@app.post("/logout")
def logout():

    session_id = request.headers.get(
        "Session-Id"
    )

    redis_client.delete(
        f"session:{session_id}"
    )

    return {
        "message": "logged out"
    }

@app.get("/limited")
def limited():

    ip = request.remote_addr

    key = f"rate:{ip}"

    count = redis_client.incr(key)

    if count == 1:
        redis_client.expire(key, 60)

    if count > 5:
        return {"message": "Too many requests"}, 429

    return {"message": "allowed"}

if __name__ == "__main__":
    app.run(debug=True)
