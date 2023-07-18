from platform import release, system
from sys import platform, version

from discord import Message
from discord import __version__ as discord_version
from psutil import Process

from dibug.classes.command import DibugCommand
from dibug.version import __version__ as dibug_version


class InfoCommand(DibugCommand):
    aliases = ["info", "i"]

    async def execute(self, msg: Message, args: str) -> None:
        lines: list[str] = []

        lines.append(f"Python `{version}` on `{system()} {release()} ({platform})`")

        lines.append(f"dibug `{dibug_version}`, discord.py `{discord_version}`")

        lines.append("")

        process = Process()
        lines.append(
            f"Process started at <t:{int(process.create_time())}:R>, PID {process.pid}, using {round(process.memory_info().rss / 2 ** 20, 2)}MB of memory"
        )

        shards = self._client.shard_count
        lines.append(
            f"This bot is {'not ' if not shards else ''}sharded{f' ({shards})' if shards else ''} and running on {len(self._client.guilds)} guild(s) with {len(self._client.users)} user(s)"
        )

        lines.append("")

        non_default_intents: list[str] = []
        for intent in self._client.intents:
            if intent[0] in ["presences", "members", "message_content"] and intent[1]:
                non_default_intents.append(intent[0])

        if non_default_intents:
            lines.append(f"Non-default intents: {', '.join(non_default_intents)}")

        lines.append(f"Latency: {round(self._client.latency * 1000, 2)}ms")

        await msg.reply("\n".join(lines))
