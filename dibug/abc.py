from abc import ABC

from discord import Message


class DibugCommandABC(ABC):
    def __init__(self, name: list[str]) -> None:
        self.name = name

    async def execute(self, msg: Message, args: str) -> None:
        ...
