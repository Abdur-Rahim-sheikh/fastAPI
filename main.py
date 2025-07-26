from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user


# this will work seamlessly,
# dropping the password field from the response
# as it is not included in the UserOut model
# But if we had added it as return type, editor would complain
# also, response_model has higher priority than return type in fastAPI
