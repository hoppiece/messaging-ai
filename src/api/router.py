from fastapi import APIRouter

from api.controllers import app, webhook

api_router = APIRouter()
api_router.include_router(app.router, tags=["health check"])
api_router.include_router(webhook.router, tags=["webhook"])
