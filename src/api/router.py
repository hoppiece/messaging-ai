from fastapi import APIRouter

from api.controllers import handler

api_router = APIRouter()
api_router.include_router(handler.router, tags=["health check"])
