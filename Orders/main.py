import time
from fastapi.background import BackgroundTasks
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
import requests
from Order import Order
from Redis_Config import redis

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:3000'], allow_methods=['*'], allow_headers=['*'])


@app.post("/orders")
async def create_order(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    req = requests.get('http://localhost:8000/products/%s' % body['id'])
    product = req.json()
    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )
    order.save()
    background_tasks.add_task(order_completed, order)

    return order


def order_completed(order: Order):
    time.sleep(10)
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed', order.dict(), '*')


@app.get('orders/{pk}')
def get_order(pk: str):
    return Order.get(pk)


@app.get('orders/')
def get_all_orders():
    return [format_orders(pk) for pk in Order.all_pks()]


def format_orders(pk: str):
    order = Order.get(pk)
    return {
        'id': order.pk,
        'product_id': order.product_id,
        'quantity': order.quantity,
        'total': order.total,
        'status': order.status
    }


