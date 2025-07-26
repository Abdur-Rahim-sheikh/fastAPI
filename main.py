from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException


async def global_dependency(x_token: Annotated[str, Header()]):
    if x_token != "fake-global-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


app = FastAPI(dependencies=[Depends(global_dependency)])


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


# depencies just to verify


async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/product/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_products():
    return [{"item": "Foo"}, {"item": "Bar"}]
