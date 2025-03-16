from contextlib import asynccontextmanager

from databases import database
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers.employee import router as employee_router

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(employee_router, prefix="/api/v1/employee")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health-check")
async def health_check():
    return "The API service is running!"
