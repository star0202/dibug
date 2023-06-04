from platform import release, system
from sys import platform, version

from discord import Client, Message, __version__
from pkg_resources import get_distribution
from psutil import Process

from ..abc import DibugCommand


class InfoCommand(DibugCommand):
    def __init__(self, name: list[str], client: Client) -> None:
        self.name = name

        self.__client = client

    async def execute(self, msg: Message, args: str) -> None:
        lines: list[str] = []

        lines.append(f"Python `{version}` on `{system()} {release()} ({platform})`")

        lines.append(
            f"dibug `{get_distribution('dibug').version}`, discord.py `{__version__}`"
        )

        lines.append("")

        process = Process()
        lines.append(
            f"Process started at <t:{int(process.create_time())}:R>, PID {process.pid}, using {round(process.memory_info().rss / 2 ** 20, 2)}MB of memory"
        )

        shards = self.__client.shard_count
        lines.append(
            f"This bot is {'not ' if not shards else ''}sharded{f' ({shards})' if shards else ''} and running on {len(self.__client.guilds)} guild(s) with {len(self.__client.users)} user(s)"
        )

        lines.append("")

        non_default_intents: list[str] = []
        for intent in self.__client.intents:
            if intent[0] in ["presences", "members", "message_content"] and intent[1]:
                non_default_intents.append(intent[0])

        if non_default_intents:
            lines.append(f"Non-default intents: {', '.join(non_default_intents)}")

        lines.append(f"Latency: {round(self.__client.latency * 1000, 2)}ms")

        await msg.reply("\n".join(lines))
