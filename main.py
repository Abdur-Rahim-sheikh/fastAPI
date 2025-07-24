from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/{price}")
async def create_item(item: Item, item2: Item, price: int, name: str):
    item.name = name or item.name
    item.price = price
    return item
