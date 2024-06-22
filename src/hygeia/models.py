from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    status: str = "OK"


class RichmenuCreateResponse(BaseModel):
    rich_menu_id: str
