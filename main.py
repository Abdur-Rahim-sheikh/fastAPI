from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


class CommonQueryParams:
    def __init__(self, q: str = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/")
async def read_items(commons: Annotated[CommonQueryParams, Depends()]):
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[CommonQueryParams, Depends(use_cache=False)]):
    return commons
