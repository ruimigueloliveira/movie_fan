from fastapi import FastAPI
from registry.users_operations import register
import registry.users_operations as u

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# FIXME Use POST and pass password in request body instead of in endpoint
# FIXME password is already received in hash form
@app.get("/v1/signup/{username}/{email}/{password}")
async def signup(username, email, password) -> dict:
    # If signup successful
    status: int = register(username, email, password)
    if status != u.OK:
        return {"message": f"Error: {u.status_code(status)}"}
    return {"message": "OK"}


@app.get("/v1/login/{username}/{email}/{password}")
async def login(username, email, password) -> dict:
    # If signup successful
    status: int = u.check(username, email, password)
    if status == u.OK:
        return {"message": f"Error: {u.status_code(status)}"}
    return {"message": "OK"}

