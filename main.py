from fastapi import FastAPI
from .routes import users
from .routes import auth
from .routes import requests

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(requests.router)


@app.get("/")
def root():
    return {"message": "API работает"}
