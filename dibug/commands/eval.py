from traceback import format_exception

from async_eval import eval
from discord import Client, Message

from ..abc import DibugCommand
from ..utils import DibugEmbed, inspect


class EvalCommand(DibugCommand):
    def __init__(self, name: list[str], client: Client) -> None:
        self.name = name

        self.__client = client

    async def execute(self, msg: Message, args: str) -> None:
        if not args:
            await msg.reply("Missing code")
            return

        res = await msg.reply("Running...")

        if args.startswith("```py") and args.endswith("```"):
            args = args[6:-3]

        try:
            result = eval(args, {"client": self.__client, "msg": msg})

            embed = (
                DibugEmbed("Eval")
                .chunked_fields(
                    "Input",
                    args,
                    "py",
                )
                .chunked_fields(
                    "Output (Verbose)",
                    "\n".join(inspect(result, 0)),
                    "py",
                )
                .chunked_fields(
                    "Output (Compact)",
                    str(result),
                    "py",
                )
            )

            await res.edit(content=None, embed=embed)

        except Exception as e:
            embed = (
                DibugEmbed("Eval", True)
                .chunked_fields(
                    "Input",
                    args,
                    "py",
                )
                .chunked_fields(
                    "Error",
                    "\n".join(format_exception(e)),
                    "py",
                )
            )

            await res.edit(content=None, embed=embed)
