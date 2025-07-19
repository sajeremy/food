from fastapi import FastAPI

from router import v0

app = FastAPI(title="Food API")


app.include_router(v0.router, prefix="/api")
