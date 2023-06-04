from abc import ABC
from typing import Any

from discord import Message


class DibugCommand(ABC):
    name: str

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        ...

    async def execute(self, msg: Message, args: str) -> None:
        ...
