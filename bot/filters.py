from aiogram.filters import BaseFilter
from aiogram.types import Message

from data import ADMINS


class Admin(BaseFilter):
    def __init__(self):
        self.admins = ADMINS

    async def __call__(self, message: Message) -> bool:
        return (message.from_user.id in self.admins or message.from_user.username in self.admins) and message.chat.type=="private"

