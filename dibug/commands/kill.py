from discord import Message
from psutil import Process

from ..abc import DibugCommandABC


class KillCommand(DibugCommandABC):
    def __init__(self, name: list[str]) -> None:
        self.name = name

    async def execute(self, msg: Message, args: str) -> None:
        await msg.reply("Shutting down...")

        process = Process()
        process.kill()
