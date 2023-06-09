from typing import Any, Callable, Coroutine, Literal, Type

from discord import Client, Message

from .abc import DibugCommandABC
from .commands import EvalCommand, InfoCommand, KillCommand, ShellCommand


class Dibugger:
    """
    A debugger for discord.py bots.

    Parameters
    ----------
    client : Client
        The discord.py client to attach the debugger to.
    user_has_perm : Callable[[Message], Coroutine[Any, Any, bool]]
        A function that returns whether the user has permission to use the debugger.
    no_perm_msg : str
        The message to send when the user doesn't have permission, by default "No Permission".
    prefix : str
        The prefix for the debugger, by default "!dbg".
    default : Literal["info", "kill"]
        The default command to run when no command is specified, command shouldn't have any arguments, by default "info".
    patch_on_init : bool
        Whether to patch the client on init, by default True.
        If False, you will have to manually call :meth:`handle_msg` on every message, and every edited message if you want.

    Methods
    -------
    handle_msg(msg: Message)
        Handle a message and execute the command if it exists.
    """

    def __init__(
        self,
        client: Client,
        user_has_perm: Callable[[Message], Coroutine[Any, Any, bool]],
        no_perm_msg: str = "No Permission",
        prefix: str = "!dbg",
        default: Literal["info", "kill"] = "info",
        patch_on_init: bool = True,
    ):
        self.client = client
        self.user_has_perm = user_has_perm
        self.no_perm_msg = no_perm_msg
        self.prefix = prefix
        self.default = default
        self.patch_on_init = patch_on_init

        self._commands: list[DibugCommandABC] = []

        self._register_command(EvalCommand, ["eval", "e", "python", "py"], self.client)
        self._register_command(InfoCommand, ["info", "i"], self.client)
        self._register_command(KillCommand, ["kill", "k", "shutdown"])
        self._register_command(ShellCommand, ["shell", "sh"])

        if self.patch_on_init:
            if hasattr(self.client, "on_message"):
                original_func = getattr(self.client, "on_message")

                async def on_message_patch(msg: Message) -> None:
                    await original_func(msg)
                    await self.handle_msg(msg)

            else:

                async def on_message_patch(msg: Message) -> None:
                    await self.handle_msg(msg)

            setattr(self.client, "on_message", on_message_patch)

            if hasattr(self.client, "on_message_edit"):
                original_func = getattr(self.client, "on_message_edit")

                async def on_message_edit_patch(
                    before: Message, after: Message
                ) -> None:
                    await original_func(before, after)
                    await self.handle_msg(after)

            else:

                async def on_message_edit_patch(
                    before: Message, after: Message
                ) -> None:
                    await self.handle_msg(after)

            setattr(self.client, "on_message_edit", on_message_edit_patch)

    def _register_command(
        self, command: Type[DibugCommandABC], name: list[str], *args: Any, **kwargs: Any
    ) -> None:
        self._commands.append(command(name, *args, **kwargs))

    async def handle_msg(self, msg: Message) -> None:
        """
        Handle a message and execute the command if it exists.

        Parameters
        ----------
        msg : Message
            The message to handle.

        Returns
        -------
        None
        """

        if msg.author.bot or not msg.content.startswith(self.prefix):
            return

        if not await self.user_has_perm(msg):
            await msg.reply(self.no_perm_msg)
            return

        cmd = msg.content[len(self.prefix) :].split()

        if not cmd:
            cmd = [self.default]

        for command in self._commands:
            for name in command.name:
                if cmd[0] == name:
                    await command.execute(msg, " ".join(cmd[1:]))
                    return
