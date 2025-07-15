from fastapi import FastAPI

from router import v0

app = FastAPI()
app.include_router(v0.router, prefix="/api")
