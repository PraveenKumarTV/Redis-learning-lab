from flask import Flask
from redis_client import redis_client
import time
import json

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
    
if __name__ == "__main__":
    app.run(debug=True)
