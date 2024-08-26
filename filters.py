from aiogram.filters import BaseFilter
from aiogram.types import Message

from sql_queries import is_in_users


class IsAuthorizedUser(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return is_in_users(message)
