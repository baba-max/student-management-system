from fastapi import FastAPI, APIRouter
from user_router import user_router

app = FastAPI()

app.include_router(user_router)