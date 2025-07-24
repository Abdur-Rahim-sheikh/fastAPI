### FastAPI iteration

#### request body parsing

```python
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return item
```

This code defines a FastAPI application with a single endpoint that accepts a POST request with a JSON body. The body is parsed into an `Item` model defined using Pydantic, which provides data validation and serialization.
Just declaring a type let's see what fastapi does with it:

1. Read the body of the request as JSON.
2. Convert the corresponding types (if needed).
3. Validate the data.
   - If the data is invalid, it will return a nice and clear error, indicating exactly where and what was the incorrect data.
4. Give you the received data in the parameter `item`
   - As you declared it in the function to be of type Item, you will also have all the editor support (completion, etc) for all of the attributes and their types.
5. Generate JSON Schema definitions for your model, you can also use them anywhere else you like if it makes sense for your project.
6. Those schemas will be part of the generated OpenAPI schema, and used by the automatic documentation UIs.
