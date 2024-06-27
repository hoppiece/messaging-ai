from logging import getLogger

from linebot.v3.webhooks import (
    JoinEvent,
    LeaveEvent,
    MemberJoinedEvent,
    MemberLeftEvent,
    UnfollowEvent,
    UnsendEvent,
)

from hygeia.botconf import handler, hygeia_user
from hygeia.repositories import crud

logger = getLogger("uvicorn.app")


@handler.add(UnsendEvent)
async def hadle_unsend(event: UnsendEvent) -> None:  # type: ignore[no-any-unimported]
    logger.info(
        f"UnsendEvent. user_id: {event.source.user_id} group_id: {event.source.group_id} message_id: {event.unsend.message_id}"
    )


@handler.add(UnfollowEvent)
async def handle_unfollow(event: UnfollowEvent) -> None:  # type: ignore[no-any-unimported]
    logger.info(f"UnfollowEvent. user_id: {event.source.user_id}")
    user_id: str = event.source.user_id
    crud.delete_user(hygeia_user, user_id)


@handler.add(JoinEvent)
async def handle_join(event: JoinEvent) -> None:  # type: ignore[no-any-unimported]
    logger.info(f"JoinEvent. group_id: {event.source.group_id}")


@handler.add(LeaveEvent)
async def handle_leave(event: LeaveEvent) -> None:  # type: ignore[no-any-unimported]
    logger.info(f"LeaveEvent. group_id: {event.source.group_id}")


@handler.add(MemberJoinedEvent)
async def handle_member_join(event: MemberJoinedEvent) -> None:  # type: ignore[no-any-unimported]
    logger.info(f"MemverJoinEvent. {event.source.group_id}")


@handler.add(MemberLeftEvent)
async def handle_member_left(event: MemberLeftEvent) -> None:  # type: ignore[no-any-unimported]
    logger.info(f"MemverLeftEvent. {event.source.group_id}")
