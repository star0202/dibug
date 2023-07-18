from discord import Message
from psutil import Process

from . import DibugCommand


class KillCommand(DibugCommand):
    async def execute(self, msg: Message, args: str) -> None:
        await msg.reply("Shutting down...")

        process = Process()
        process.kill()
