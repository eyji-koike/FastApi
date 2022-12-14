import time
from Product import Product
from Redis_Config import redis

key = 'order_completed'
group = 'inventory_group'

try:
    redis.xgroup_create(key, group)
except Exception as e:
    print('Group Already Exists! ' + str(e))

while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)

        if results:
            for result in results:
                obj = result[1][0][1]
                try:
                    product = Product.get(obj['product_id'])
                    product.quantity = product.quantity - int(obj['quantity'])
                    product.save()
                except Exception as e:
                    print(str(e))
                    redis.xadd('refund_order', obj, '*')

    except Exception as e:
        print(str(e))

    time.sleep(1)
