from decouple import config
from redis_om import get_redis_connection

redis = get_redis_connection(
    host=config('HOST'),
    port=config('PORT'),
    password=config('PASS'),
    decode_responses=True
)
