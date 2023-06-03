from typing import Any, Callable, Type

from discord import Client, Message

from .abc import DibugCommand
from .commands import EvalCommand


class Dibugger:
    def __init__(
        self,
        client: Client,
        is_owner: Callable[[int], bool],
        no_perm_msg: str = "No Permission",
        prefix: str = "!dbg ",
    ):
        self.client = client
        self.is_owner = is_owner
        self.no_perm_msg = no_perm_msg
        self.prefix = prefix

        self.__commands: list[DibugCommand] = []

        self.__register_command(EvalCommand, client)

    def __register_command(
        self, command: Type[DibugCommand], *args: Any, **kwargs: Any
    ) -> None:
        self.__commands.append(command(*args, **kwargs))

    async def handle_msg(self, msg: Message) -> None:
        if msg.author.bot or not msg.content.startswith(self.prefix):
            return

        if not self.is_owner(msg.author.id):
            await msg.channel.send(self.no_perm_msg)
            return

        cmd = msg.content[len(self.prefix) + 1 :]

        for command in self.__commands:
            if cmd.startswith(command.name):
                await command.execute(msg, cmd[len(command.name) + 1 :])
