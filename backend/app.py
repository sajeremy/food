from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router import v0

app = FastAPI(title="Food API")
# Vite development server
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/openapi.json")
def get_openapi_schema():
    return app.openapi()


app.include_router(v0.router, prefix="/api")
