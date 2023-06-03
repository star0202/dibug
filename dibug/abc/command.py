from abc import ABC

from discord import Message


class DibugCommand(ABC):
    name: str

    async def execute(self, msg: Message, args: str) -> None:
        ...
