from subprocess import run

from discord import Message

from ..abc import DibugCommand
from ..utils import DibugEmbed


class ShellCommand(DibugCommand):
    def __init__(self, name: list[str]) -> None:
        self.name = name

    async def execute(self, msg: Message, args: str) -> None:
        if not args:
            await msg.reply("Missing code")
            return

        res = await msg.reply("Running...")

        if args.startswith("```sh") and args.endswith("```"):
            args = args[6:-3]

        result = run(args, capture_output=True, shell=True, text=True)

        if result.stderr:
            embed = (
                DibugEmbed("Shell", True)
                .chunked_fields(
                    "Input",
                    args,
                    "sh",
                )
                .chunked_fields(
                    "Error",
                    result.stderr,
                    "sh",
                )
            )

            await res.edit(content=None, embed=embed)
            return

        embed = (
            DibugEmbed("Shell")
            .chunked_fields(
                "Input",
                args,
                "sh",
            )
            .chunked_fields(
                "Output",
                result.stdout,
                "sh",
            )
        )

        await res.edit(content=None, embed=embed)
