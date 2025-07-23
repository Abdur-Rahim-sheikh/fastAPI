from enum import Enum

from fastapi import FastAPI

app = FastAPI()


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/files/{file_path:path}/other")
async def read_file(file_path: str):
    return {"file_path": file_path}
