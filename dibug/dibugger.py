from __future__ import annotations

from typing import Any, Callable, Coroutine, Type

from discord import Client, Message

from dibug.classes.command import DibugCommand
from dibug.commands import commands


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
    patch_on_init : bool
        Whether to patch the client on init, by default True.
        If False, you will have to manually call :meth:`handle_msg` on every message, and every edited message if you want.

    Methods
    -------
    handle_msg(msg: Message)
        Handle a message and execute the command if it exists.

    Class Methods
    --------------
    attach(
        client: Client,
        user_has_perm: Callable[[Message], Coroutine[Any, Any, bool]],
        no_perm_msg: str = "No Permission",
        prefix: str = "!dbg",
        patch_on_init: bool = True,
    ) -> Dibugger
        Attach a debugger to a discord.py client.
    """

    def __init__(
        self,
        client: Client,
        user_has_perm: Callable[[Message], Coroutine[Any, Any, bool]],
        no_perm_msg: str = "No Permission",
        prefix: str = "!dbg",
        patch_on_init: bool = True,
    ) -> None:
        self.client = client
        self.user_has_perm = user_has_perm
        self.no_perm_msg = no_perm_msg
        self.prefix = prefix
        self.patch_on_init = patch_on_init

        self._commands: list[DibugCommand] = []

        for command in commands:
            self._register_command(
                command,
                self.client,
            )

        if self.patch_on_init:
            setattr(self.client, "on_message", self.handle_msg)

            async def handle_edited_msg(_: Any, after: Message) -> None:
                await self.handle_msg(after)

            setattr(self.client, "on_message_edit", handle_edited_msg)

    def _register_command(self, command: Type[DibugCommand], client: Client) -> None:
        self._commands.append(command(client))

    @classmethod
    def attach(
        cls,
        client: Client,
        user_has_perm: Callable[[Message], Coroutine[Any, Any, bool]],
        no_perm_msg: str = "No Permission",
        prefix: str = "!dbg",
        patch_on_init: bool = True,
    ) -> Dibugger:
        """
        Attach a debugger to a discord.py client.

        Parameters
        ----------
        client : Client
            The discord.py client to attach the debugger to.
        user_has_perm : Callable[[Message], Coroutine[Any, Any, bool]]
            A function that returns whether the user has permission to use the debugger.
        no_perm_msg : str, optional
            The message to send when the user doesn't have permission, by default "No Permission".
        prefix : str, optional
            The prefix for the debugger, by default "!dbg".
        patch_on_init : bool, optional
            Whether to patch the client on init, by default True.
            If False, you will have to manually call :meth:`handle_msg` on every message, and every edited message if you want.

        Returns
        -------
        Dibugger
            The debugger that was attached.
        """

        return cls(
            client,
            user_has_perm,
            no_perm_msg,
            prefix,
            patch_on_init,
        )

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

        cmd = msg.content[len(self.prefix) :]

        for command in self._commands:
            for name in command.aliases:
                if cmd.startswith(name):
                    await command.execute(msg, cmd[len(name) :])
                    return
