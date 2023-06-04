from subprocess import run

from discord import Message

from ..abc import DibugCommand
from ..utils import chunked_fields, shell_embed


class ShellCommand(DibugCommand):
    def __init__(self, name: list[str]) -> None:
        self.name = name

    async def execute(self, msg: Message, args: str) -> None:
        if not args:
            await msg.channel.send("No codes")
            return

        res = await msg.reply("Running...")

        if args.startswith("```sh") and args.endswith("```"):
            args = args[5:-3]

        result = run(args, capture_output=True, shell=True, text=True)

        if result.stderr:
            embed = shell_embed(args, 0xFF0000)

            chunked_fields(
                embed,
                "Error",
                "sh",
                result.stderr,
                1024 - 10,
            )

            await res.edit(content=None, embed=embed)
            return

        embed = shell_embed(args, 0x2B2D31)

        chunked_fields(
            embed,
            "Output",
            "sh",
            result.stdout,
            1024 - 10,
        )

        await res.edit(content=None, embed=embed)
