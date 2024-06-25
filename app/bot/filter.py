from aiogram.filters import BaseFilter
from aiogram.types import Message
from app.core.settings import get_settings


class IsUser(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        client = get_settings().app.get_client
        me = await client.get_me()
        return message.from_user == me.id