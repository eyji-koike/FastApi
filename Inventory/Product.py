from redis_om import HashModel
from Redis_Config import redis


class Product(HashModel):
    name: str
    price: int
    quantity: int

    class Meta:
        database = redis
