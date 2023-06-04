from traceback import format_exception

from async_eval import eval
from discord import Client, Message

from ..abc import DibugCommand
from ..utils import chunked_fields, eval_embed, inspect


class EvalCommand(DibugCommand):
    def __init__(self, name: list[str], client: Client) -> None:
        self.name = name
        self.client = client

    async def execute(self, msg: Message, args: str) -> None:
        if not args:
            await msg.channel.send("No codes")
            return

        res = await msg.reply("Running...")

        if args.startswith("```py") and args.endswith("```"):
            args = args[5:-3]

        try:
            result = eval(args, {"client": self.client, "msg": msg})

            embed = eval_embed(args, 0x2B2D31)

            chunked_fields(
                embed,
                "Output (Verbose)",
                "py",
                "\n".join(inspect(result, 0)),
                1024 - 10,
            )

            chunked_fields(
                embed,
                "Output (Compact)",
                "py",
                str(result),
                1024 - 10,
            )

            await res.edit(content=None, embed=embed)

        except Exception as e:
            embed = eval_embed(args, 0xFF0000)

            chunked_fields(
                embed, "Error", "py", "".join(format_exception(e)), 1024 - 10
            )

            await res.edit(content=None, embed=embed)
