from discord import Message

from .eval import EvalCommand
from .info import InfoCommand
from .kill import KillCommand
from .shell import ShellCommand

__all__ = ["EvalCommand", "InfoCommand", "KillCommand", "ShellCommand"]


class DibugCommand:
    def __init__(self, name: list[str]) -> None:
        self.name = name

    async def execute(self, msg: Message, args: str) -> None:
        raise NotImplementedError
