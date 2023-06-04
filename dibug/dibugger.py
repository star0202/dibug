from typing import Any, Callable, Coroutine, Literal, Type

from discord import Client, Message

from .abc import DibugCommand
from .commands import EvalCommand, InfoCommand, KillCommand, ShellCommand


class Dibugger:
    def __init__(
        self,
        client: Client,
        user_has_perm: Callable[[Message], Coroutine[Any, Any, bool]],
        no_perm_msg: str = "No Permission",
        prefix: str = "!dbg",
        default: Literal["info"] = "info",
    ):
        self.client = client
        self.user_has_perm = user_has_perm
        self.no_perm_msg = no_perm_msg
        self.prefix = prefix
        self.default = default

        self.__commands: list[DibugCommand] = []

        self.__register_command(EvalCommand, ["eval", "e", "python", "py"], self.client)
        self.__register_command(InfoCommand, ["info", "i"], self.client)
        self.__register_command(KillCommand, ["kill", "k", "shutdown"])
        self.__register_command(ShellCommand, ["shell", "sh"])

        if hasattr(self.client, "on_message"):
            original_func = getattr(self.client, "on_message")

            async def patch(msg: Message) -> None:
                await original_func(msg)
                await self.handle_msg(msg)

        else:

            async def patch(msg: Message) -> None:
                await self.handle_msg(msg)

        setattr(self.client, "on_message", patch)

    def __register_command(
        self, command: Type[DibugCommand], name: list[str], *args: Any, **kwargs: Any
    ) -> None:
        self.__commands.append(command(name, *args, **kwargs))

    async def handle_msg(self, msg: Message) -> None:
        if msg.author.bot or not msg.content.startswith(self.prefix):
            return

        if not await self.user_has_perm(msg):
            await msg.reply(self.no_perm_msg)
            return

        cmd = msg.content[len(self.prefix) :].split()

        if not cmd:
            cmd = [self.default]

        for command in self.__commands:
            for name in command.name:
                if cmd[0] == name:
                    await command.execute(msg, " ".join(cmd[1:]))
                    return
