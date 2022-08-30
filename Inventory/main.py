from decouple import config
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from Product import Product

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:3000'], allow_methods=['*'], allow_headers=['*'])


@app.get("/products")
def all_products():
    return [format_products(pk) for pk in Product.all_pks()]


def format_products(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }


@app.post("/products")
def create_product(product: Product):
    return product.save()


@app.get("/products/{pk}")
def get_product(pk: str):
    return Product.get(pk)


@app.delete("/products/{pk}")
def delete(pk: str):
    product = Product.get(pk)
    return product.delete()
