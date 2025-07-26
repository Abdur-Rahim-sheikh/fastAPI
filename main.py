from fastapi import FastAPI, Response
from pydantic import BaseModel, EmailStr
from fastapi.responses import JSONResponse, RedirectResponse

app = FastAPI()


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(BaseUser):
    password: str


@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user


# this will work seamlessly,
# dropping the password field from the response
# as it is not included in the UserOut model
# But if we had added it as return type, editor would complain
# also, response_model has higher priority than return type in fastAPI


@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://abir-interactive-study.streamlit.app/")
    return JSONResponse(
        content={
            "message": "Welcome to the portal! Use the teleport query parameter to access the interactive study."
        }
    )
