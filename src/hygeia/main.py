from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from hygeia.config import settings
from hygeia.controllers import health_check, modify_bot, webhook

api_router = APIRouter()
api_router.include_router(health_check.router, tags=["health check"])
api_router.include_router(webhook.router, tags=["webhook"])
api_router.include_router(modify_bot.router, tags=["settings"])


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ALLOW_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
