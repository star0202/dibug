from discord import Message
from psutil import Process

from ..abc import DibugCommandABC


class KillCommand(DibugCommandABC):
    async def execute(self, msg: Message, args: str) -> None:
        await msg.reply("Shutting down...")

        process = Process()
        process.kill()
