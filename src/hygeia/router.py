from fastapi import APIRouter

from hygeia.controllers import health_check, webhook

api_router = APIRouter()
api_router.include_router(health_check.router, tags=["health check"])
api_router.include_router(webhook.router, tags=["webhook"])
