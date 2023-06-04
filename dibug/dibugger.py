from typing import Any, Callable, Type

from discord import Client, Message

from .abc import DibugCommand
from .commands import EvalCommand, ShellCommand


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
        self.__register_command(ShellCommand, ["shell", "sh"])

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

        cmd = msg.content[len(self.prefix) :].split()

        for command in self.__commands:
            for name in command.name:
                if cmd[0] == name:
                    await command.execute(msg, " ".join(cmd[1:]))
                    return
