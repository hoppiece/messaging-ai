from fastapi import APIRouter

from api import controller

api_router = APIRouter()
api_router.include_router(controller.router, tags=["health check"])
