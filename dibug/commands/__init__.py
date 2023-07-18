from dibug.classes.command import DibugCommand
from dibug.commands.eval import EvalCommand
from dibug.commands.info import InfoCommand
from dibug.commands.kill import KillCommand
from dibug.commands.shell import ShellCommand

commands: list[type[DibugCommand]] = [
    EvalCommand,
    InfoCommand,
    KillCommand,
    ShellCommand,
]
