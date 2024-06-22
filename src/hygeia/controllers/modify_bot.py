from fastapi import APIRouter

from hygeia.models import RichmenuCreateResponse
from hygeia.views import rich_menu

router = APIRouter()


@router.post("/rich_menus", response_model=RichmenuCreateResponse)
async def create_rich_menu() -> RichmenuCreateResponse:
    rich_menu_id = await rich_menu.set_rich_menu()
    return RichmenuCreateResponse(rich_menu_id=rich_menu_id)


@router.delete("/rich_menus")
async def delete_rich_menu() -> None:
    await rich_menu.delete_rich_menu()
