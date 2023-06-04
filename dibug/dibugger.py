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

        self.__register_command(EvalCommand, ["eval", "e", "python", "py"], client)

    def __register_command(
        self, command: Type[DibugCommand], name: list[str], *args: Any, **kwargs: Any
    ) -> None:
        self.__commands.append(command(name, *args, **kwargs))

    async def handle_msg(self, msg: Message) -> None:
        if msg.author.bot or not msg.content.startswith(self.prefix):
            return

        if not self.is_owner(msg.author.id):
            await msg.channel.send(self.no_perm_msg)
            return

        cmd = msg.content[len(self.prefix) :]

        for command in self.__commands:
            for name in command.name:
                if cmd.startswith(name):
                    await command.execute(msg, cmd[len(name) + 1 :])
